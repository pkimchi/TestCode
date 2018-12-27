function calc()
{
  $.ajax(
    {
      type:"POST",
      data:{
        "val1":$("#02").val(),
        "val2":$("#03").val(),
        "val3":$("#04").val(),
        "val4":$("#05").val(),
        "tvalue":$("input[name='tvalue']:checked").val(),
        "val6":$("#06").val(),
        "val7":$("#07").val(),
        "val8":$("#08").val(),
        "val9":$('#09').val(),
        "val10":$('#10').val(),

        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
      },
      success:function(data)

      {
        $("#sample_size").text("min sample size per variation is: " + data["result"])

        if ($("#06").val() !="")
          $("#days_required").text("estimated days to run your test: " + data["resultsdays"])
//        $("#test").text("this is a test")

        $("#lift_treatment").text("relative uplift result: " + data["resultslift"] + "%")
      }
    }
  )
}
