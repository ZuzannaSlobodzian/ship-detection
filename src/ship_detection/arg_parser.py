import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Write arguments:")
    parser.add_argument("--start_date", "-sd", required=False, help="Date of start detecting, f.e. '2020-07-06'", default='2020-07-06')
    parser.add_argument("--end_date", "-ed", required=False, help="End date of detecting, f.e. '2020-08-09'", default='2020-08-09')
    
    return parser.parse_args()