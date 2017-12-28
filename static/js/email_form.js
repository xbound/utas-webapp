var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
function csrfSafeMethod(method)
{
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function removeTask(pk)
{
  $.ajax(
    {
      url: '/remove/',
      type: 'POST',
      data: {'pk':pk},
      beforeSend: function(xhr, settings)
      {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain)
        {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      },
      success: function(response)
      {
        if(response.success)
        {
          $('#info-success').text(response.info);
          $('#success').modal("show");
        }
        else
        {
          $('#info-failure').text(response.info);
          $('#failure').modal("show");
        }
      }
    });
  return false;
}
