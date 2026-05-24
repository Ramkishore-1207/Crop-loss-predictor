import streamlit as st
import joblib
import numpy as np

model = joblib.load('crop_yield_model_small.pkl')
