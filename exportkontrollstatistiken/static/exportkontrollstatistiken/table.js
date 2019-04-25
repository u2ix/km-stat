table = {
  initialize : function(params){
    this.dataCounter = 0;
    this.params = params;

    this.table = d3.select('div.table table');
    this.thead = this.table.select("thead");
    this.tbody = this.table.select("tbody");
    
    // TODO: Make empty table more sensible/prettier
    const loading = 'loading';
    const row = [loading, loading, loading, loading];
    rows = [];
    for(var i=0; i<this.params.params.perPage; i++){
      rows.push(row);
    }
    data = {
      cnames : row,
      data : rows,
    }
    this.setData(0, data);

    this.setRemoteData();
  },
  setRemoteData : function(){
    this.dataCounter++;
    d3.json(this.params.url).then(data => this.setData(this.dataCounter, data));
    // TODO: Display some data change/loading indicator.
  },
  setData : function(number, data) {
    if(this.dataCounter>number){
      // some other data was requested in the mean time, so this
      // data set is discarded
      console.log('discarding data set ' + number);
      return;
    }
    // TODO: Set up navigation drop down, disable buttons that don't make sense

    // set up page selection only if we aren't on the first pseudo data set
    if(number!=0){
      this.numberOfPages = Math.ceil(data.total / this.params.params.perPage);

      //drop down
      pageList = [];
      for(var page=1; page<=this.numberOfPages; page++){
        pageList.push(page);
      }
      d3.selectAll('#table_jumpToPage option').remove();
      pageDropDown=d3.select('#table_jumpToPage');
      pageDropDown
        .selectAll('option')
        .data(pageList)
        .enter()
        .append('option')
          .text(d => "Gehe zu Seite " + d)
          .attr('value', d=>d)
          .attr('selected', d => {
            if(d==this.params.params.pageNumber){
              return true;
            }else{
              return null;
            }
          });
      pageDropDown.on('change', () => {
        this.params.params.pageNumber = pageDropDown.property("value");
        this.params.recalculateURL();
        this.setRemoteData();
      });

      // deactivate some buttons
      onFirstPage = this.params.params.pageNumber == 1;
      if(!onFirstPage){onFirstPage=null;}
      onLastPage = this.params.params.pageNumber == this.numberOfPages;
      if(!onLastPage){onLastPage=null;}
      // deactivate the two back buttons
      d3.select('#table_firstPage').attr('disabled', onFirstPage);
      d3.select('#table_previousPage').attr('disabled', onFirstPage);
      // deactivate the two forward buttons
      d3.select('#table_lastPage').attr('disabled', onLastPage);
      d3.select('#table_nextPage').attr('disabled', onLastPage);
    }
    
    /*
     * The following snippet was copied from the d3 doc on .data()
     * */
    
    this.thead
      .selectAll("tr")
      .data([data['cnames']])
      .join("tr")
      .selectAll("td")
      .data(d => d)
      .join("td")
        .text(d => d);
    // TODO: Array rows are somehow mixed. The order is not random, but seems like multiple correctly sorted parts interleaved. Columns stay correct.
    // TODO: This started working correctly again. Find out why.
    this.tbody
      .selectAll("tr")
      .data(data['data'])
      .join("tr")
      .selectAll("td")
      .data(d => d)
      .join("td")
        .text(d => d);
  },
  firstPage : function(){
    this.params.params.pageNumber = 1;
    this.params.recalculateURL();
    this.setRemoteData();
  },
  previousPage : function(){
    this.params.params.pageNumber = Math.max(1, this.params.params.pageNumber-1);
    this.params.recalculateURL();
    this.setRemoteData();
  },
  nextPage : function(){
    this.params.params.pageNumber = Math.min(this.numberOfPages, this.params.params.pageNumber+1);
    this.params.recalculateURL();
    this.setRemoteData();
  },
  lastPage : function(){
    this.params.params.pageNumber = this.numberOfPages;
    this.params.recalculateURL();
    this.setRemoteData();
  },
}
