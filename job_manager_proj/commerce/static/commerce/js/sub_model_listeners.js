document.addEventListener('DOMContentLoaded', function () {
    let idPrefix = 'id_planned_business_trips';
    var parentElement = document.getElementById('planned_business_trips-group');
    parentElement.addEventListener('input', function (event) {
        var target = event.target;

        if (target.id && target.id.startsWith(idPrefix) && target.id.endsWith('-day_count')) {
            updateTotalCost();
        }
        if (target.id && target.id.startsWith(idPrefix) && target.id.endsWith('-staff_count')) {
            updateTotalCost();
        }
        if (target.id && target.id.startsWith(idPrefix) && target.id.endsWith('-lodging_cost')) {
            updateTotalCost();
        }
        if (target.id && target.id.startsWith(idPrefix) && target.id.endsWith('-public_transportation_fare')) {
            updateTotalCost();
        }
        if (target.id && target.id.startsWith(idPrefix) && target.id.endsWith('-one_way_distance_on_company_transport')) {
            updateTotalCost();
        }
    });
});