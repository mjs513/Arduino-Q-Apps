from arduino.app_bricks.streamlit_ui import st
from arduino.app_utils import *
import pandas as pd
import numpy as np

def main():
  # Create initial DataFrame
  df1 = pd.DataFrame(np.random.randn(50, 20), columns=(f'col {i}' for i in range(20)))
  
  # Display the initial line chart
  my_chart = st.line_chart(df1)
  
  # Create additional DataFrame
  df2 = pd.DataFrame(np.random.randn(50, 20), columns=(f'col {i}' for i in range(20)))
  
  # Add more data to the existing chart
  my_chart.add_rows(df2)


if __name__ == "__main__":
    main()
