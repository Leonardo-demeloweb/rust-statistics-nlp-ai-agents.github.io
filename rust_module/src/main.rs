use serde::{Deserialize, Serialize};
use std::io::{self, Read};

mod statistics;

#[derive(Deserialize)]
struct InputData {
    data: Vec<f64>,
}

#[derive(Serialize)]
struct StatisticsResult {
    min: f64,
    max: f64,
    mean: f64,
    median: f64,
    q1: f64,
    q3: f64,
    std_dev: f64,
    coef_var: f64,
}

fn main() {
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer).unwrap();

    let input_data: InputData = serde_json::from_str(&buffer).unwrap();
    let result = statistics::compute_statistics(input_data.data);

    let json_result = serde_json::to_string(&result).unwrap();
    println!("{}", json_result);
}
