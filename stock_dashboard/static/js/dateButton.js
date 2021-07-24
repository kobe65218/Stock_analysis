      $("button#dateButton").click(() => {
          var stock_id = $("input#search").val()
          location.href= "http:/?stock_id="+stock_id

      })

      $("button#searchbutton").click(() => {
          var stock_id = $("input#search").val()
          location.href= "http:/?stock_id="+stock_id

      })

      $("button#dateButton").click(() => {
          var stock_id = $("input#search").val()
          var start = $("input#start").val()
          var end = $("input#end").val()
          location.href= "http:/?stock_id="+stock_id + "&start=" +start + "&end=" + end


      })
