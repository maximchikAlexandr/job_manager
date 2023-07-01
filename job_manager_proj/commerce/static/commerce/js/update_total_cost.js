function updateTotalCost() {
    var mileage = 0;
    var travel_expenses = 0;

    let idPrefix = 'id_planned_business_trips';
    const fields = document.querySelectorAll(`input[id^="${idPrefix}"][id$="day_count"]`);
    let len = fields.length;

    if (len > 0) {
        for (let i = 0; i < len - 1; i++) {
            let distance = parseFloat(document.getElementById(`${idPrefix}-${i}-one_way_distance_on_company_transport`).value);
            mileage += distance;

            let day_count = parseFloat(document.getElementById(`${idPrefix}-${i}-day_count`).value);
            let staff_count = parseFloat(document.getElementById((`${idPrefix}-${i}-staff_count`)).value);
            let lodging_cost = parseFloat(document.getElementById((`${idPrefix}-${i}-lodging_cost`)).value);
            let public_transportation_fare = parseFloat(document.getElementById((`${idPrefix}-${i}-public_transportation_fare`)).value);
            travel_expenses += (day_count * staff_count * 9 + lodging_cost + public_transportation_fare);
        }
    }
    travel_expenses = Math.ceil(travel_expenses);
    var transportation_expenses = Math.ceil(0.5630625 * mileage);
    var workload = parseFloat(document.getElementById('id_workload').value);
    var hourlyRate = parseFloat(document.getElementById('id_hourly_rate').value);
    var outsourcing_costs = parseFloat(document.getElementById('id_outsourcing_costs').value);
    var profit = parseFloat(document.getElementById('id_profit').value);


    var salary = Math.ceil(workload * hourlyRate);
    var income_taxes = Math.ceil(0.13 * salary);
    var social_security_contributions = Math.ceil(0.34 * salary);
    var overhead_expenses = Math.ceil(1.6 * salary);
    var depreciation_expenses = Math.ceil(0.175 * salary);
    var accident_insurance = Math.ceil(0.006 * salary);

    var cost_price = (
        salary
        + income_taxes
        + social_security_contributions
        + overhead_expenses
        + depreciation_expenses
        + transportation_expenses
        + accident_insurance
        + travel_expenses
    );
    var price_excluding_vat = cost_price * ((100 + profit) / 100) + outsourcing_costs;
    var vat = 0.2 * price_excluding_vat;
    var selling_price_including_vat = price_excluding_vat + vat;

    var totalCostElement = document.querySelector('.form-row.field-total_cost .flex-container' +
        ' .readonly');

    totalCostElement.textContent = selling_price_including_vat.toFixed(2);
}
