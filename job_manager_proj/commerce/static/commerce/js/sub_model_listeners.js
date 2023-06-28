document.addEventListener('DOMContentLoaded', function() {
  const idPrefix = 'id_planned_business_trips';
  const parentElement = document.getElementById('planned_business_trips-group');
  parentElement.addEventListener('input', function(event) {
    const target = event.target;
    const id = target.id;

    if (id && id.startsWith(idPrefix)) {
      const suffix = id.substring(id.lastIndexOf('-') + 1);

      if (['day_count', 'staff_count', 'lodging_cost', 'public_transportation_fare', 'one_way_distance_on_company_transport'].includes(suffix)) {
        updateTotalCost();
      }
    }
  });
});