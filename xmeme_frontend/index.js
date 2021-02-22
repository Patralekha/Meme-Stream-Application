//function to render a meme or a collection of memes inside a div on index.html
function loop(data, str) {
  var i;
  for (i = 0; i < data.length; i++) {
    var modalId = "modal" + data[i]["id"];
    var formId = "form" + data[i]["id"];
    var datar = "#" + modalId;
    var updatedId = "upmeme" + data[i]["id"];
    var updatedUrl = "url" + data[i]["id"];
    var updatedUrl1 = "#" + updatedUrl;
    var updatedCaption = "caption" + data[i]["id"];
    var updatedCaption1 = "#" + updatedCaption;
    var dateTime = new Date(data[i]["creationDateTime"])
      .toString()
      .substring(0, 25);
    var lastUpdate = new Date(data[i]["lastUpdate"])
      .toString()
      .substring(0, 25);

    $(str).append(
      `
                  <div class="card md-6 text-black bg-light">
                  
                  <div class="card-body">
                    <div class="card-title" >
                        <h2>${data[i]["name"]}<p style="float: right;font-size: small;"></p></h2>
                        
                    </div>
                    <p class="card-text"><small class="text-muted"><strong>Last updated on:</strong><br/>${lastUpdate}</small><a class="btn btn-warning"  data-toggle="modal" data-target="${datar}" style="float: right;color:black">Edit&nbsp;<i class='fas fa-edit' style='font-size:18px;'></i></a></p>
                    <p class="card-text"><small class="text-muted"><strong>Created on:</strong><br/>${dateTime}</small></p>
                    <p class="card-text">${data[i]["caption"]}</p>
                    
                    
                  </div>
                  <hr>
                  
                  <img class="card-img-bottom" src="${data[i]["url"]}" alt="Meme image">
                </div><br/><br/>


                <div class="modal fade" id="${modalId}" "tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Edit your meme</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
      <form id="${formId}" method="post" name="${formId}">
      <input id="${updatedId}" name="${updatedId}" type="hidden" value="${data[i]["id"]}">
      <label for="exampleFormControlTextarea1" style="font-weight: bolder;color:burlywood;">Meme Caption</label>
      <textarea  class="form-control" id="${updatedCaption}" name="${updatedCaption}" row="6">${data[i]["caption"]}</textarea>
      <label for="exampleFormControlInput1" style="font-weight: bolder;color:burlywood;">Meme image URL</label>
      <input type="url" id="${updatedUrl}" name="${updatedUrl}" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" value="${data[i]["url"]}">
      <br/>
      
      <a  class="btn btn-primary" onclick="updateMemeFunction($('input[name=${updatedUrl}]').val(),$('textarea[name=${updatedCaption}]').val(),$('input[name=${updatedId}]').val())" >Save changes</a>
      </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>

   
                  `
    );
  }
}


//function to load latest 100 memes on a page
function loadMemes() {
  document.getElementById("allmemes").innerHTML = "";
  $.ajax({
    type: "GET",
    url: "https://cryptic-lake-25546.herokuapp.com/memefilters/getAllMemes",
    success: function (data) {
      loop(data, "#allmemes");
    },
    error: function (response) {
      alert(response["statusText"]);
    },
  });
}



//function to update a particular meme,either its caption or url or both
function updateMemeFunction(url1, caption1, id) {
  console.log(caption1);
  console.log(url1);
  console.log(id);

  document.getElementById("allmemes").innerHTML = "";
  var urlt =
    "https://cryptic-lake-25546.herokuapp.com/memefilters/" +
    id +
    "/updateMeme";

  fetch(urlt, {
    method: "PATCH",
    body: JSON.stringify({
      url: url1,
      caption: caption1,
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8",
    },
  })
    .then(function (response) {
      console.log(response);
      if (!response.ok) {
        alert(response.statusText);
        return "notok";
      }
      return "ok";
    })
    .then(function (responseData) {
      if (responseData === "notok") {
        console.log("Bad response from server.");
      } else window.location.reload();
    });
}



//function to check if id input while searching a meme by id is a positive integer or not
function isNumberKey(evt) {
  var charCode = evt.which ? evt.which : evt.keyCode;
  if (charCode > 31 && (charCode < 48 || charCode > 57))
    alert("Enter a positive number for meme id");
}


//function to check url whether input while creating a meme or editing a meme is valid image url or not
function checkURL(url) {
  return url.match(/\.(jpeg|jpg|gif|png)$/) != null;
}




//function to retrieve a meme by id when search meme form is submitted
$(document).ready(function () {
  $("#searchMemeForm").submit(function (event) {
    /* stop form from submitting normally */
    event.preventDefault();
    var memeId = $("input[name=memeSearchId]").val();
    document.getElementsByName("searchMemeForm")[0].reset();
    if (isNaN(memeId)) {
      alert("Please enter a positive number!!!!");
      return false;
    }

    document.getElementById("allmemes").innerHTML = "";

    var formData = $(this).serialize();

    $.ajax({
      type: "GET",
      url:
        "https://cryptic-lake-25546.herokuapp.com/memefilters/" +
        memeId +
        "/getMeme",
      success: function (data) {
        loop(data, "#allmemes");
      },
      error: function (response) {
        alert(response["statusText"]);
      },
    });
  });
});



//function to create a meme,triggered when createMeme form is submitted successfully
$(document).ready(function () {
  $("#createMeme").submit(function (event) {
    /* stop form from submitting normally */
    event.preventDefault();

    var url = $("input[name=url]").val();
    if (!checkURL(url)) {
      alert("Enter a valid  image url that ends with jpeg/jpg/gif/png");
      //return false;
    } else {
      var formData = $(this).serialize();

      console.log(formData);
      document.getElementsByName("createMeme")[0].reset();
      $.ajax({
        type: "POST",
        url: "https://cryptic-lake-25546.herokuapp.com/memefilters/createMeme",
        data: formData,
        success: function (result) {
          console.log(result);
          loadMemes();
        },
        error: function (response) {
          alert(response["statusText"]);
        },
      });
    }
  });
});




//function to search for memes with a given creator name
$(document).ready(function () {
  $("#filterByNameForm").submit(function (event) {
    /* stop form from submitting normally */
    event.preventDefault();
    var name1 = $("input[name=namefilter]").val();

    console.log(name1);

    document.getElementById("allmemes").innerHTML = "";
    document.getElementsByName("filterByNameForm")[0].reset();

    var formData = $(this).serialize();
    fetch("https://cryptic-lake-25546.herokuapp.com/memefilters/byName", {
      method: "POST",
      body: JSON.stringify({
        name: name1,
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8",
      },
    })
      .then(function (response) {
        console.log(response);
        if (!response.ok) {
          alert("Creator name not found!!");
          console.log(response.statusText);
          return {};
        }
        return response.json();
      })
      .then(function (responseData) {
        if (responseData.length == 0) {
          console.log("Bad response from server.");
          //alert('Creator name not found!!');
        } else loop(responseData, "#allmemes");
      });
  });
});


//function to search for memes created within range of dates input
$(document).ready(function () {
  $("#filterByDateForm").submit(function (event) {
    /* stop form from submitting normally */
    event.preventDefault();
    var start = $("input[name=startdate]").val();
    var end = $("input[name=enddate]").val();
   console.log(start+" "+end);
    if (start > end) {
      alert("End date cannot be before start date");
      document.getElementsByName("filterByDateForm")[0].reset();
    } else {
      document.getElementById("allmemes").innerHTML = "";
      document.getElementsByName("filterByDateForm")[0].reset();
      fetch(
        "https://cryptic-lake-25546.herokuapp.com/memefilters/byDateRange",
        {
          method: "POST",
          body: JSON.stringify({
            startDate: start,
            endDate: end,
          }),
          headers: {
            "Content-type": "application/json; charset=UTF-8",
          },
        }
      )
        .then(function (response) {
          console.log(response);
          if (!response.ok) {
            alert(response.statusText);
            return {};
          }
          return response.json();
        })
        .then(function (responseData) {
          if (responseData.length == 0) {
            console.log("Bad response from server.");
          } else loop(responseData, "#allmemes");
        });
    }
  });
});
