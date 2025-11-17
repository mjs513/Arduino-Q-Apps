import matplotlib.pyplot as plt
import numpy as np

from arduino.app_bricks.streamlit_ui import st
from arduino.app_utils import *

def main():
  # Streamlit app title
  st.title("📊 Streamlit + Matplotlib Example")
  
  # Sidebar controls for interactivity
  st.sidebar.header("Plot Controls")
  freq = st.sidebar.slider("Frequency (Hz)", min_value=1, max_value=20, value=5, step=1)
  amp = st.sidebar.slider("Amplitude", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
  
  # Generate data
  x = np.linspace(0, 2 * np.pi, 500)
  y = amp * np.sin(freq * x)
  
  # Create Matplotlib figure
  fig, ax = plt.subplots()
  ax.plot(x, y, label=f"{amp} × sin({freq}x)")
  ax.set_title("Sine Wave")
  ax.set_xlabel("x")
  ax.set_ylabel("y")
  ax.grid(True)
  ax.legend()
  
  # Display plot in Streamlit
  st.pyplot(fig)
  
  # Optional: Show data table
  if st.checkbox("Show data table"):
      st.dataframe({"x": x, "y": y})

if __name__ == "__main__":
    main()
