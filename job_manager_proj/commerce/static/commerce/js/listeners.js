document.addEventListener('DOMContentLoaded', function() {
document.getElementById('id_workload').addEventListener('input', updateTotalCost);
document.getElementById('id_hourly_rate').addEventListener('input', updateTotalCost);
document.getElementById('id_outsourcing_costs').addEventListener('input', updateTotalCost);
document.getElementById('id_profit_percentage').addEventListener('input', updateTotalCost);
  });
