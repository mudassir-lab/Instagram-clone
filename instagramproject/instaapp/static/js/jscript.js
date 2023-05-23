$(document).ready(function () {

  $(".like-button").click(function (e) {
    e.preventDefault();
    var post_id = $(this).attr('data-post-id');
    $.ajax({
      url: '/likes/' + post_id,
      type: 'GET',
      data: { CSRF: '{{csrf_token}}' },
      dataType: 'json',
      success: function (response) {

        console.log(response);

        // console.log($('.like-button').html());
        // console.log(typeof($('.like-button').html()))

        if ($('#like-button-' + post_id).html().includes('<i class="far fa-heart"></i>')) {
          $('#like-button-' + post_id).html('<i class="fas fa-heart" style="color: red"></i>');  // change the button to a red heart
        }
        else {
          $('#like-button-' + post_id).html('<i class="far fa-heart"></i>');  // change the button to a white heart
        }

        $('#likes-count-' + post_id).text(response.likes_count + " likes")

        // console.log($('.like-button').html());
      }
    });
  });



  $(".follow-button").click(function (e) {
    e.preventDefault();
    var username = $(this).attr('data-profile-username');
    $.ajax({
      url: '/follow/' + username,
      type: 'GET',
      data: { CSRF: '{{csrf_token}}' },
      dataType: 'json',
      success: function (response) {

        console.log(response);

        // console.log($('.like-button').html());
        // console.log(typeof($('.like-button').html()))

        if ($('.follow-button').text().includes('Follow')) {
          $('.follow-button').text('Unfollow');  // change the button to a red heart
        }
        else {
          $('.follow-button').text('Follow');  // change the button to a white heart
        }

        $('.followers_count-number').text(response.followers_count)

        // console.log($('.like-button').html());
      }
    });
  });


  $(document).ready(function () {
    $('.reply').click(function () {
      var commentId = $(this).parent().data('id');  // get the ID of the clicked comment
      var user = $(this).parent().data('user');
      // set the value of the parent field in the form to the comment ID
      $('.comment-form').find('input[name="parent"]').val(commentId);
      $('.comment-form').find('input[name="comment"]').attr('placeholder', 'Reply to ' + user);
    });
  });


  $(document).ready(function () {
    $('.story').click(function () {
      var story_src = $(this).attr('data-story-src');
      var story_id = $(this).attr('data-story-id');

      console.log(story_src)
      document.getElementById("fullscreenimg").setAttribute("src", story_src);
      document.getElementById("fullscreenimg").style.display = "block";
      document.getElementById("main").style.display = "none";
      document.getElementById("story-" + story_id).style.borderColor = "lightgrey";

    });

    $('#fullscreenimg').click(function () {

      document.getElementById("fullscreenimg").style.display = "none";
      document.getElementById("main").style.display = "block";

    });

  });


});