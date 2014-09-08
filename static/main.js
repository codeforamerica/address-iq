if(typeof String.prototype.trim !== 'function') {
  String.prototype.trim = function() {
    return this.replace(/^\s+|\s+$/g, ''); 
  }
}

$(document).ready(function() {

  var fillContentTab = function(department, timeframe) {

    var formatTopCallTypeInfo = function(topCallType, idx) {
      // Takes an array, where first el is call type, second is
      // count of how many there were in given timeframe
      // Idx is the index into the list
      // Returns an li

      var text = (idx + 1) + ". " + topCallType[0].trim() + " - " + topCallType[1] + ' calls';

      var $el = $('<li>');
      $el.text(text);

      if ((idx + 1) % 2 == 0) {
        $el.addClass('even');
      } else {
        $el.addClass('odd');
      }

      return $el;
    }

    callTypes = topCallTypes[department][timeframe]


    $callTypesOl = $('.call-types');
    $('.call-types').html('');
    $('.no-calls-of-this-type').hide();

    if (callTypes.length == 0) {
      $('.no-calls-of-this-type').show();
    }

    for(var i = 0; i < callTypes.length; i++) {
      var newEl = formatTopCallTypeInfo(callTypes[i], i);
      $callTypesOl.append(newEl);
    }

  }

  var updateContentTab = function() {
    var department = $('.department-tab.active').attr('id').slice(4);
    var timeframe = $('#data-date-range').val();
    fillContentTab(department, timeframe);    
  }

  $('.department-tab').click(function() {
    var $tab = $(this);
    if($tab.hasClass('active')) return;

    $('.department-tab.active').removeClass('active');
    $tab.addClass('active');

    updateContentTab();
  });

  $('#data-date-range').change(updateContentTab);

  // Make browse page rows clickable
  $('#browse-page tbody tr').click(function() {
    window.location.href = $(this).find('.explore-link a').attr('href');
    return false;
  });

  // Activation on the address page
  $('#activated-toggle').click(function() {
    var $toggle = $(this);
    var activated = $toggle.hasClass('activated');

    var action = activated ? '//deactivate' : '//activate';
    var url = window.location.pathname + action;

    $.ajax({
      url: url,
      method: 'POST',
      data: {
        "_csrf_token": csrfToken
      },
      success: function(data) {
        $toggle.removeClass('activated');
        $toggle.removeClass('deactivated');

        $toggle.addClass(data);
      },
      error: function(data) {
        alert('Activation did not succeed. Please try again or refresh the page.');
      }
    })

  });


  $('.search-area form').submit(function() {
    var address = $(this).find('input').val();

    window.location.pathname = '//address/' + address;
    return false;
  });

// Adapted from https://github.com/codeforamerica/bizarro-cms/blob/0d2e3cea116e054eb1e2ebbd2787175fa6c09923/bizarro/static/script.js

  function simpleXhrSentinel(xhr) {

      return function() {
          if (xhr.readyState == 4) {
              if (xhr.status == 200){
                  // reload page to reflect new login state
                  if (typeof window.next !== 'undefined' && window.next != 'None') {
                    window.location.assign(window.next);
                    // Now clear the 'next' variable.
                    window.next = 'None';
                  }
                  else {
                    window.location.reload();
                  }
                }
              else {
                  navigator.id.logout();
                  alert("We weren't able to log you in. Please try again or contact the AddressIQ administrator to ensure you have permission to access the site.");
                }
              }
            }
          }

  function verifyAssertion(assertion) {
      // Your backend must return HTTP status code 200 to indicate successful
      // verification of user's email address and it must arrange for the binding
      // of currentUser to said address when the page is reloaded
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "//log-in", true);
      // see http://www.openjs.com/articles/ajax_xmlhttp_using_post.php
      var param = "assertion="+assertion;
      xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
      xhr.setRequestHeader("Content-length", param.length);
      xhr.setRequestHeader("Connection", "close");
      xhr.send(param); // for verification by your backend

      xhr.onreadystatechange = simpleXhrSentinel(xhr); }

  function signoutUser() {
      // Your backend must return HTTP status code 200 to indicate successful
      // logout (usually the resetting of one or more session variables) and
      // it must arrange for the binding of currentUser to 'null' when the page
      // is reloaded
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "//log-out", true);
      xhr.send(null);
      xhr.onreadystatechange = simpleXhrSentinel(xhr); }

  // Go!
  navigator.id.watch( {
      loggedInUser: currentUser,
      onlogin: verifyAssertion,
      onlogout: signoutUser } );
});

