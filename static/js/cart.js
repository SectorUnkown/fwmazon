// Generated by CoffeeScript 1.6.3
(function() {
  var $, Cart;

  $ = jQuery;

  Cart = (function() {
    function Cart() {
      this.get_cookie();
      this.init_ajax();
      this.init_events();
    }

    Cart.prototype.get_cookie = function() {
      return this.csrftoken = $.cookie('csrftoken');
    };

    Cart.prototype.csrf_safe_method = function(method) {
      return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
    };

    Cart.prototype.init_ajax = function() {
      var _this = this;
      return $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
          if (!_this.csrf_safe_method(settings.type)) {
            return xhr.setRequestHeader('X-CSRFToken', _this.csrftoken);
          }
        }
      });
    };

    Cart.prototype.init_events = function() {
      $('body').on('click', 'a#add-to-cart', this.add);
      $('body').on('click', 'a#update-cart', this.update);
      return $('body').on('click', 'a#delete-from-cart', this["delete"]);
    };

    Cart.prototype.add = function(e) {
      var amount, id, req, type;
      e.preventDefault();
      id = $(this).data('id');
      type = $(this).data('type');
      amount = $("input[data-id=" + id + "][data-type=" + type + "]").val();
      if (amount === 0 || amount < 0) {
        return;
      }
      req = $.ajax({
        url: '/shop/cart/add',
        type: 'POST',
        data: {
          'item_id': id,
          'item_type': type,
          'amount': amount
        }
      });
      req.done(function(data) {
        return window.location.reload();
      });
      return req.error(function(data) {
        return show_error('An error occured while updating the shopping cart, please try again');
      });
    };

    Cart.prototype.update = function(e) {
      var amount, id, req, type;
      e.preventDefault();
      id = $(this).data('id');
      type = $(this).data('type');
      amount = $("input[data-id=" + id + "][data-type=" + type + "]").val();
      if (amount < 0) {
        return;
      }
      req = $.ajax({
        url: '/shop/cart/update',
        type: 'POST',
        data: {
          'item_id': id,
          'item_type': type,
          'amount': amount
        }
      });
      req.done(function(data) {
        return window.location.reload();
      });
      return req.error(function(data) {
        return show_error('An error occured while updating the shopping cart, please try again');
      });
    };

    Cart.prototype["delete"] = function(e) {
      var id, req, type;
      e.preventDefault();
      id = $(this).data('id');
      type = $(this).data('type');
      req = $.ajax({
        url: '/shop/cart/delete',
        type: 'POST',
        data: {
          'item_id': id,
          'item_type': type
        }
      });
      req.done(function(data) {
        return window.location.reload();
      });
      return req.error(function(data) {
        return show_error('An error occured while updating the shopping cart, please try again');
      });
    };

    return Cart;

  })();

  window.show_error = function(message) {
    var id;
    id = Math.floor(Math.random() * 100);
    $('#messages').append("<div class=\"alert alert-danger\" id=\"message-" + id + "\">" + message + "</div>");
    return setTimeout(function() {
      return hide_message(id);
    }, 5000);
  };

  window.hide_message = function(id) {
    return $("#messages #message-" + id).remove();
  };

  $(document).on('ready', function() {
    return window.cart = new Cart();
  });

}).call(this);
