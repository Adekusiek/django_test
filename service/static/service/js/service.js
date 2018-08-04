function getValue(varName){
  var paramsArray;
  var prevMonth=0;

  paramsArray = location.search.split('?', 2);
  for(var i=0; i< paramsArray.length; i++){
    if (paramsArray[i].split('=')[0] == varName){
      return paramsArray[i].split('=')[1];
    }
  }
  return null;
}

function set_prev_month(){
    var prev_month = 0;
    if(getValue('prev_month')) prev_month = getValue('prev_month');
    return prev_month;
}
