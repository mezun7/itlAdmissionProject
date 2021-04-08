Chart.pluginService.register({
    beforeDraw: function (chart) {
        var width = chart.chart.width,
            height = chart.chart.height,
            ctx = chart.chart.ctx;
        ctx.restore();
        var fontSize = (height / 114).toFixed(2);
        ctx.font = fontSize + "em sans-serif";
        ctx.textBaseline = "middle";
        var text = chart.config.options.elements.center.text,
            textX = Math.round((width - ctx.measureText(text).width) / 2),
            textY = height / 2 + 15;
        ctx.fillText(text, textX, textY);
        ctx.save();
    }
});



$(function () {
    /* ChartJS
     * -------
     * Here we will create a few charts using ChartJS
     */
      var AllRegOptions     = {
      maintainAspectRatio : false,
      responsive : true,
          elements: {
      center: {
      text: '',
      color: '#36A2EB', //Default black
      fontStyle: 'Helvetica', //Default Arial
      sidePadding: 20 //Default 20 (as a percentage)
    }}

    }
   var ProfileChartCanvas = $('#profileChart').get(0).getContext('2d')
    var ProfileData = {}
    var ProfileOptions = {}
   $.ajax({

    url: "/api/profile/",
    dataType: "json",
     async: false,
    success: function (data){
        ProfileData = data['data']
        ProfileOptions = data['options']
    }
  })

    //Create pie or douhnut chart
    // You can switch between pie and douhnut using the method below.
    new Chart(ProfileChartCanvas, {
      type: 'doughnut',
      data: ProfileData,
      options: ProfileOptions
    })

    var AllRegChartCanvas = $('#donutAllRegistrations').get(0).getContext('2d')
    var AllRegData = {}
    var RegOptions = {}
   $.ajax({

    url: "/api/all/",
    dataType: "json",
     async: false,
    success: function (data){
        AllRegData = data['data']
        RegOptions = data['options']
    }
  })

    //Create pie or douhnut chart
    // You can switch between pie and douhnut using the method below.
    new Chart(AllRegChartCanvas, {
      type: 'doughnut',
      data: AllRegData,
      options: RegOptions
    })

    //-------------
    //- PIE CHART -
    //-------------
    // Get context with jQuery - using jQuery's .get() method.

    var GenderChartCanvas = $('#genderChart').get(0).getContext('2d')
    var genderData        = {}
    var genderOptions = {}
      $.ajax({

    url: "/api/gender/",
    dataType: "json",
     async: false,
    success: function (data){
        genderData = data['data']
        genderOptions = data['options']
    }
  })

    //Create pie or douhnut chart
    // You can switch between pie and douhnut using the method below.
    new Chart(GenderChartCanvas, {
      type: 'doughnut',
      data: genderData,
      options: genderOptions
    })


    var CompetitionChartCanvas = $('#competitionChart').get(0).getContext('2d')
    var compData = {}
    var compOptions = {}
      $.ajax({

    url: "/api/reg_status/",
    dataType: "json",
     async: false,
    success: function (data){
        compData = data['data']
        compOptions = data['options']
    }
  })

    //Create pie or douhnut chart
    // You can switch between pie and douhnut using the method below.
    new Chart(CompetitionChartCanvas, {
      type: 'doughnut',
      data: compData,
      options: compOptions
    })

    var DatesChartCanvas = $('#datesChart').get(0).getContext('2d')
    var datesData = {}
    var datesOptions = {}
      $.ajax({

    url: "/api/dates/",
    dataType: "json",
     async: false,
    success: function (data){
        datesData = data['data']
        datesOptions = data['options']
    }
  })

    //Create pie or douhnut chart
    // You can switch between pie and douhnut using the method below.
    new Chart(DatesChartCanvas, {
      type: 'doughnut',
      data: datesData,
      options: datesOptions
    })
  })