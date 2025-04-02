use super::StatisticsResult;

pub fn compute_statistics(data: Vec<f64>) -> StatisticsResult {
    let min = data.iter().cloned().fold(f64::INFINITY, f64::min);
    let max = data.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let mean = data.iter().sum::<f64>() / data.len() as f64;

    let mut sorted = data.clone();
    sorted.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let median = sorted[sorted.len() / 2];

    let q1 = sorted[sorted.len() / 4];
    let q3 = sorted[(sorted.len() * 3) / 4];

    let variance = data.iter().map(|v| (v - mean).powi(2)).sum::<f64>() / data.len() as f64;
    let std_dev = variance.sqrt();
    let coef_var = std_dev / mean;

    StatisticsResult {
        min,
        max,
        mean,
        median,
        q1,
        q3,
        std_dev,
        coef_var,
    }
}
