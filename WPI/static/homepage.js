function openForm(name) {
  document.getElementById(name).style.display = "block";
}
function closeForm(name) {
  document.getElementById(name).style.display = "none";
}


function openDialog(review){
    document.getElementById('light').style.display='block';
    document.getElementById('fade').style.display='block';
    document.getElementById("attractionName").value=attractionName;
    document.getElementById("review_id").value=review.review_id;
    document.getElementById("review").value=review.review;

    var select = document.getElementById('rating');
    select.value = review.rating
}

function closeDialog(){
    document.getElementById('light').style.display='none';
    document.getElementById('fade').style.display='none';
}

function closeDialogDelete(user_id){
    // console.log(user_id);
    // console.log(review_id.value);
    $.ajax({
        type: "POST",
        url: '/user/reviews/',
        data: {'method': 'delete', 'user_id': user_id, 'review_id': review_id.value},
        success : function (Response) {
            location.reload();
            },
        error: function (){
            alert("Operation Error");
        }
    })
}