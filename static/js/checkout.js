// Generated by CoffeeScript 1.6.3
var $, CostUpdater, Shipping,
  __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

$ = jQuery;

Shipping = (function() {
  function Shipping() {
    this.update_shipping = __bind(this.update_shipping, this);
    this._volume = $('span#js-volume').data('volume');
    this.init_events();
    this.update_shipping();
  }

  Shipping.prototype.init_events = function() {
    return $('body').on('change', 'select#shipping', this.update_shipping);
  };

  Shipping.prototype.update_shipping = function(e) {
    var $option, cost, delay, total_shipping;
    $option = $('select#shipping').children(':selected');
    cost = parseFloat($option.data('cost'));
    delay = parseFloat($option.data('delay'));
    total_shipping = cost * this._volume;
    $('span#js-shipping-cost').text(to_comma(total_shipping)).data('cost', total_shipping);
    return $('body').trigger('cost_update');
  };

  return Shipping;

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

window.to_comma = function(int) {
  return int.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};

CostUpdater = (function() {
  function CostUpdater() {
    this.update_price = __bind(this.update_price, this);
    this.fitting = $('span#js-fitting-price').data('price');
    $('body').on('cost_update', this.update_price);
    $('body').on('change', 'input#fitting', this.update_price);
  }

  CostUpdater.prototype.update_price = function() {
    this.collect_prices();
    $('span#js-review-shipping').text(to_comma(this.prices.shipping));
    $('span#js-review-options').text(to_comma(this.prices.options));
    $('span#js-review-tax').text(to_comma(this.prices.tax));
    return $('span#js-review-total').text(to_comma(this.prices.total));
  };

  CostUpdater.prototype.collect_prices = function() {
    this.prices.sub_total = parseFloat($('span#js-review-subtotal').data('subtotal'));
    this.prices.shipping = parseFloat($('span#js-shipping-cost').data('cost'));
    if ($('input#fitting').prop('checked')) {
      this.prices.options = this.fitting;
    } else {
      this.prices.options = 0.0;
    }
    this.prices.tax = (this.prices.sub_total + this.prices.shipping + this.prices.options) * 0.05;
    return this.prices.total = this.prices.sub_total + this.prices.shipping + this.prices.options + this.prices.tax;
  };

  CostUpdater.prototype.prices = {
    'sub_total': 0.0,
    'shipping': 0.0,
    'options': 0.0,
    'tax': 0.0,
    'total': 0.0
  };

  return CostUpdater;

})();

$(document).on('ready', function() {
  window.cost_updater = new CostUpdater();
  return window.shipping = new Shipping();
});
