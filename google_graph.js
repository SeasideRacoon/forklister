  var span = document.getElementById("fork");
var forks_json = forks_graph.dataset.json;
json_dict = JSON.parse(forks_json);
forks_array = json_dict.forks;
var dataBJ = [['ID', 'days ago', 'ahead by', 'behind by', 'stargazers', 'url' ]] ;
var days = [];
forks_array.forEach
(function(elem)
{dataBJ.push([elem.url.replace('https://github.com/', '')
.split('/')[0], elem.days_ago, elem.ahead_by, elem.behind_by, elem.stargazers, elem.url]);
days.push(elem.days_ago);
});
  google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawSeriesChart);

    function drawSeriesChart() {

      var data = google.visualization.arrayToDataTable(dataBJ);

  //    var view = new google.visualization.DataView(data);
  //`    view.setColumns([0, 1, 2, 3, 4]);

      var options = {
        title: 'behind by',
        hAxis: {title: 'days ago', minValue: Math.min.apply(null, days) - 10},
        vAxis: {title: 'ahead by', minValue: -10},
                colorAxis: {colors: ['red', 'grey']},
     bubble: {textStyle: {fontSize: 11}}
      };

      var chart = new google.visualization.BubbleChart(document.getElementById('series_chart_div'));

      google.visualization.events.addListener(chart, 'select', function ()
      {
      var selection = chart.getSelection();  // get selected slice

      // ensure something is selected
      if (selection.length > 0)
      {
      // open the site
      window.open(data.getValue(selection[0].row, 5), '_blank');
      console.log(data.getValue(selection[0].row, 5));
      }
      });

      chart.draw(data, options);
    }