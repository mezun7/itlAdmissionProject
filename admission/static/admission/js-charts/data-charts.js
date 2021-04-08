$(function () {
    /* ChartJS
     * -------
     * Here we will create a few charts using ChartJS
     */
      var AllRegOptions     = {
      maintainAspectRatio : false,
      responsive : true,
    }
   var ProfileChartCanvas = $('#profileChart').get(0).getContext('2d')
    var ProfileData = {};
   $.ajax({

    url: "/api/profile/",
    dataType: "json",
     async: false,
    success: function (data){
        ProfileData = data
    }
  })

    //Create pie or douhnut chart
    // You can switch between pie and douhnut using the method below.
    new Chart(ProfileChartCanvas, {
      type: 'doughnut',
      data: ProfileData,
      options: AllRegOptions
    })

    var AllRegChartCanvas = $('#donutAllRegistrations').get(0).getContext('2d')
    var AllRegData = {};
   $.ajax({

    url: "/api/all/",
    dataType: "json",
     async: false,
    success: function (data){
        AllRegData = data
    }
  })

    //Create pie or douhnut chart
    // You can switch between pie and douhnut using the method below.
    new Chart(AllRegChartCanvas, {
      type: 'doughnut',
      data: AllRegData,
      options: AllRegOptions
    })

    //-------------
    //- PIE CHART -
    //-------------
    // Get context with jQuery - using jQuery's .get() method.

    var GenderChartCanvas = $('#genderChart').get(0).getContext('2d')
    var genderData        = {};
      $.ajax({

    url: "/api/gender/",
    dataType: "json",
     async: false,
    success: function (data){
        genderData = data
    }
  })

    //Create pie or douhnut chart
    // You can switch between pie and douhnut using the method below.
    new Chart(GenderChartCanvas, {
      type: 'doughnut',
      data: genderData,
      options: AllRegOptions
    })


      var CompetitionChartCanvas = $('#competitionChart').get(0).getContext('2d')
    var compData        = {};
      $.ajax({

    url: "/api/reg_status/",
    dataType: "json",
     async: false,
    success: function (data){
        compData = data
    }
  })

    //Create pie or douhnut chart
    // You can switch between pie and douhnut using the method below.
    new Chart(CompetitionChartCanvas, {
      type: 'doughnut',
      data: compData,
      options: AllRegOptions
    })

          var DatesChartCanvas = $('#datesChart').get(0).getContext('2d')
    var datesData        = {};
      $.ajax({

    url: "/api/dates/",
    dataType: "json",
     async: false,
    success: function (data){
        datesData = data
    }
  })

    //Create pie or douhnut chart
    // You can switch between pie and douhnut using the method below.
    new Chart(DatesChartCanvas, {
      type: 'doughnut',
      data: datesData,
      options: AllRegOptions
    })
  })