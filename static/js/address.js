// Reload the city options of an address form when its region (province) changes
$(document).on('change', '.address-form .region-select', function () {
    var $addressForm = $(this).closest('.address-form');
    var $citySelect = $addressForm.find('.city-select');
    var regionId = $(this).val();
    var options = '<option value="">' + $addressForm.data('empty-label') + '</option>';

    if (!regionId) {
        $citySelect.html(options);
        return;
    }

    $.ajax({
        url: $addressForm.data('url'),
        data: { 'region': regionId },
        dataType: 'json',
        success: function (data) {
            $.each(data, function (index, city) {
                options += '<option value="' + city[0] + '">' + $('<div>').text(city[1]).html() + '</option>';
            });
            $citySelect.html(options);
        },
        error: function () {
            alert('Error loading cities.');
        }
    });
});
