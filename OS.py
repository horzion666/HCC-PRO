from unittest import result
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sksurv.tree import SurvivalTree
from sksurv.column import encode_categorical
from sksurv.ensemble import RandomSurvivalForest
from sksurv.ensemble import GradientBoostingSurvivalAnalysis
from sklearn.model_selection import RandomizedSearchCV
from sksurv.metrics import concordance_index_censored
from sksurv.util import Surv

dev=pd.DataFrame({
 'OS': [134.4, 11.9, 84.39, 15.4, 7.0, 80.4, 25.7, 84.3, 80.0, 56.5, 5.3, 9.5, 79.3, 60.8, 9.2, 68.61, 1.5, 19.7, 84.69, 57.3, 52.6, 36.6, 57.0, 83.0, 44.35, 88.8, 76.4, 82.1, 56.8, 26.83, 46.9, 82.75, 84.79, 62.1, 58.2, 97.25, 81.1, 14.5, 66.71, 68.65, 54.0, 109.1, 64.7, 11.0, 15.9, 78.2, 78.9, 53.3, 109.58, 71.77, 56.5, 0.9, 31.1, 4.0, 13.9, 65.59, 71.8, 66.9, 60.0, 27.8, 21.2, 70.9, 11.7, 53.3, 35.28, 88.83, 79.1, 83.1, 22.8, 161.8, 65.1, 8.7, 18.1, 111.4, 61.5, 4.2, 19.6, 83.93, 83.9, 32.4, 13.0, 63.2, 65.49, 1.0, 30.87, 72.03, 103.3, 152.9, 6.7, 131.8, 89.42, 2.6, 85.9, 1.2, 63.5, 88.0, 112.4, 4.41, 11.7, 109.51, 98.6, 67.4, 87.09, 110.4, 11.8, 85.3, 97.5, 12.3, 16.6, 40.3, 113.88, 44.6, 89.42, 134.1, 114.7, 22.13, 109.1, 96.3, 96.3, 2.7, 49.2, 5.5, 6.51, 43.0, 95.84, 81.7, 74.2, 114.54, 78.6, 44.1, 18.61, 89.26, 40.5, 146.4, 64.2, 60.9, 76.1, 131.8, 96.5, 22.6, 114.77, 108.3, 74.9, 90.1, 0.7, 1.6, 79.04, 9.4, 28.3, 117.5, 49.2, 24.6, 70.8, 117.96, 142.3, 119.6, 20.3, 45.5, 9.7, 57.3, 118.75, 89.5, 88.77, 33.1, 37.55, 18.0, 17.26, 71.7, 112.9, 23.4, 70.62, 115.9, 122.83, 119.9, 85.1, 114.5, 89.3, 23.5, 118.29, 130.3, 14.5, 86.4, 7.0, 125.79, 115.5, 73.5, 68.9, 80.6, 129.6, 93.6, 122.47, 123.81, 126.51, 115.0, 124.87, 112.18, 97.2, 65.4, 36.1, 32.3, 111.29, 117.27, 84.5, 126.25, 80.8, 3.3, 148.4, 55.1, 32.58, 29.7, 72.0, 39.7, 157.1, 10.2, 98.89, 71.0, 153.9, 87.3, 86.73, 38.5, 20.0, 159.5, 10.6, 53.8, 148.8, 13.9, 0.4, 12.5, 91.0, 86.8, 66.87, 9.7, 70.55, 68.3, 160.6, 77.3, 86.76, 98.4, 113.88, 36.3, 27.7, 53.52, 95.8, 63.5, 70.62, 56.2, 65.5, 70.4, 77.2, 91.4, 75.5, 16.0, 107.7, 85.71, 70.32, 77.7, 70.59, 5.3, 51.42, 70.85, 78.3, 1.3, 55.3, 46.0, 18.0, 6.7, 52.8, 8.3, 18.3, 69.11, 80.1, 86.2, 7.6, 1.0, 91.46, 10.1, 0.8, 65.98, 39.0, 100.0, 22.2, 97.51, 56.5, 95.97, 46.8, 53.95, 6.5, 73.4, 42.6, 58.29, 82.78, 94.68, 68.28, 13.0, 97.61, 57.9, 56.3, 82.36, 93.34, 67.13, 70.4, 93.4, 75.1, 97.22, 85.28, 90.0, 59.8, 52.47, 83.28, 55.5, 57.9, 91.69, 29.3, 22.0, 82.26, 68.71, 68.75, 93.24, 54.35, 85.97, 14.4, 115.6, 85.2, 89.03, 92.7, 57.6, 22.5, 56.4, 157.3, 53.8, 14.7, 84.7, 48.7, 54.18, 98.6, 95.8, 95.1, 63.0, 82.8, 6.8, 36.3, 86.6, 90.9, 38.7, 70.52, 20.8, 21.57, 62.0, 4.7, 5.16, 81.4, 93.17, 52.8, 96.66, 92.45, 42.6, 26.7, 89.19, 102.4, 53.0, 81.6, 22.3, 46.22, 15.0, 39.62, 58.0, 69.0, 69.34, 61.4, 55.1, 7.8, 97.1, 13.1, 73.6, 99.85, 10.59, 3.7, 14.0, 55.13, 35.2, 25.3, 100.6, 98.6, 51.7, 36.03, 94.68, 64.2, 90.8, 70.4, 1.0, 65.8, 62.6, 48.5, 95.6, 70.19, 21.3, 1.3, 92.91, 105.1, 36.9, 55.7, 18.5, 5.1, 97.8, 72.6, 85.61, 26.2, 54.0, 6.02, 32.6, 71.4, 76.1, 75.9, 67.76, 96.43, 54.6, 96.8],
 'death': ['Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Dead', 'Alive', 'Alive', 'Dead', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Dead', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Dead', 'Dead', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Dead', 'Alive', 'Dead', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Dead', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Dead', 'Alive', 'Dead', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Dead', 'Alive', 'Dead', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Dead', 'Dead', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Dead', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive', 'Alive'],
 'ki67_1': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
 'shenjing_1': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 'fenhua_2': [0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1],
 'Age_1': [1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
 'gengzu_1': [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
 'LLR_1': [0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
 'CEA_1': [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
 'Number12_1': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
 'N_stage_1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
 'N_stage_2': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
})

# 不需要独热编码的自变量
##num_cols = ['DFS', 'recurrence']
##cat_cols = list(set(dev.columns)-set(num_cols))
# 分类变量处理
##dev_dummy = pd.get_dummies(dev,drop_first=True,columns=cat_cols)
devx = dev.drop(columns=['OS','death'])#这是因变量，可以调整，OS需要去掉肝硬化，主要OS时间是两个s
devy = dev.loc[:,['OS','death']]# 整个数据集的因变量
devy['death'] = devy['death'] == 'Dead'
y_train = devy.rename(columns={'death':'event','OS':'time'})
# 训练集
X_train = devx
y_train_ = Surv.from_dataframe(
    event='event',
    time='time', 
    data=devy.rename(columns={'death':'event','OS':'time'}))

st.sidebar.header('Option')  # 添加侧边栏的大标题
# 添加每个下拉选择框并为其设置小标题



age_choice = st.sidebar.selectbox('Age<70', options=['No', 'Yes'], index=0)
n1_choice = st.sidebar.selectbox('N1', options=['No', 'Yes'], index=0)
n2_choice = st.sidebar.selectbox('N2', options=['No', 'Yes'], index=0)
Number12_choice = st.sidebar.selectbox('Lym-number', options=['≥15.2', '<15.2'], index=0)
pi_choice = st.sidebar.selectbox('Perineural Invasion', options=['No', 'Yes'], index=0)
llr_choice = st.sidebar.selectbox('LLR', options=['≤176.1', '>176.1'], index=0)
gengzu_choice = st.sidebar.selectbox('Obstruction', options=['No', 'Yes'], index=0)
cea_choice = st.sidebar.selectbox('CEA', options=['Normal', 'High'], index=0)
ki67_choice = st.sidebar.selectbox('Ki67', options=['≤50%', '>50%'], index=0)
fenhua2_choice = st.sidebar.selectbox('poor differentiation', options=['No', 'Yes'], index=0)

# 主页面可以用来展示其他内容或基于侧边栏选择的结果
#st.write(f"You selected AFP as {afp_choice}, GLR as {glr_choice}, and MVI as {mvi_choice}.")
# 将所有选择结果合并为一行显示
#choices_summary = f"AFP: {afp_choice}, GLR: {glr_choice}, MVI: {mvi_choice}, Size 5-10cm: {size1_choice}, Moderate differentiation: {grade1_choice}, Size >10cm: {size2_choice}, Poor differentiation: {grade2_choice}, MaVI: {mavi_choice}, Cirrhosis: {ganyinghua_choice}, Number: {number_choice}, Transfusion: {shuxue_choice}, Blood loss: {bleeding_choice}"
# 显示选择结果摘要
#st.write("选择结果摘要:", choices_summary)
# 将选择转换为数值
cea_value = 0 if cea_choice == 'Normal' else 1
n1_value = 0 if n1_choice == 'No' else 1
n2_value = 0 if n2_choice == 'No' else 1
llr_value = 0 if llr_choice == '≤176.1' else 1
fenhua2_value = 0 if fenhua2_choice == 'No' else 1
age_value = 0 if age_choice == 'No' else 1
pi_value = 0 if pi_choice == 'No' else 1
number12_value = 0 if Number12_choice == 'No' else 1
ki67_value = 0 if ki67_choice == 'No' else 1
gengzu_value = 0 if gengzu_choice == 'No' else 1

vad = pd.DataFrame({'ki67_1': [ki67_value],'shenjing_1': [pi_value],'fenhua_2': [fenhua2_value],'Age_1': [age_value],'LLR_1': [llr_value],'CEA_1': [cea_value], 'gengzu_1': [gengzu_value],'Number12_1': [number12_value],
                    'N_stage_1': [n1_value], 'N_stage_2': [n2_value]})
#X_test = pd.get_dummies(vad,drop_first=True,columns=cat_cols)
vad = vad[X_train.columns]
X_test = vad

st.title('Survival Prediction Calculator')


import numpy as np
RSF=RandomSurvivalForest(max_depth=7, min_samples_leaf=5, min_samples_split=9,n_estimators=100)
RSF.fit(X_train,y_train_)


# 指定的时间点，假设时间单位是月
va_times = [12, 36, 90]  # 对应于1年、3年、5年
run_button = st.button('Predict')

if run_button:
    RSFtestsurv = RSF.predict_survival_function(X_test)
    # 初始化存储预测结果的列表
    RSFtestresult_1 = []
    RSFtestresult_3 = []
    RSFtestresult_5 = []
    # 循环遍历每个测试集病例的生存函数
    for func in RSFtestsurv:
        # 计算特定时间点的生存概率
        RSFtestresult_1year = func(va_times[0])  # 12月
        RSFtestresult_3year = func(va_times[1])  # 36月
        RSFtestresult_5year = func(va_times[2])  # 60月
        # 将结果添加到列表中
        RSFtestresult_1.append(RSFtestresult_1year)
        RSFtestresult_3.append(RSFtestresult_3year)
        RSFtestresult_5.append(RSFtestresult_5year)
    
    # 设置图形大小
    plt.figure(figsize=(15, 6))  # 在这里调整图形的大小
    # 使用Matplotlib绘制生存函数的图形
    for i, surv_func in enumerate(RSFtestsurv):
        time_points = np.arange(5, 100)  # 根据需要调整时间点
        plt.step(time_points, surv_func(time_points), where="post",
                 label=f"Sample {i + 1}")
    plt.ylabel("est. probability of survival $\hat{S}(t)$")
    plt.xlabel("time $t$")
    plt.legend(loc="best")
    st.pyplot(plt)  # 显示图形


    survival_probabilities_df = pd.DataFrame({
        '1 Years OS Probability': RSFtestresult_1,
        '3 Years OS Probability': RSFtestresult_3,
        '5 Years OS Probability': RSFtestresult_5
    })
    # 使用Streamlit展示DataFrame
    
    # 将DataFrame转换为HTML，去掉索引并增加样式以调整字体大小和居中
    html = survival_probabilities_df.to_html(index=False, classes='table table-striped table-hover')

    # 使用Streamlit的Markdown功能展示带有HTML的DataFrame
    st.markdown(f"<style>.table {{font-size: 16px; text-align: center;}}</style>{html}", unsafe_allow_html=True)