# ☁️ Cloud Anomaly Detection System

Hey there! Welcome to the **Cloud Anomaly Detection** project.

Ever wondered what's going on behind the scenes in your cloud infrastructure? Sometimes things go sideways — a sudden CPU spike, unusual network traffic, or a process that just doesn't look right. That's exactly the kind of stuff this project helps you catch.

We built a system that uses **unsupervised machine learning** (specifically, an Isolation Forest) to spot unusual patterns in cloud data — no labeled datasets needed. Just feed it your metrics, and it figures out what's normal and what's not.

---

## What Can It Do?

- 🔍 **Detect anomalies automatically** — no need to manually define rules or thresholds
- ⚡ **Real-time predictions** — upload data and get instant results
- 📊 **Visual dashboard** — see your CPU, memory, disk, and network stats at a glance
- 📈 **Graphical analysis** — anomalies are highlighted right on the charts
- 🌐 **Simple web interface** — nothing fancy to install, just open a browser

---

## Under the Hood

Here's the tech stack we're working with:

| Tool | What It Does |
|------|-------------|
| **Python 3.9+** | Core language |
| **Flask** | Runs the web server |
| **Pandas** | Handles all the data wrangling |
| **Scikit-learn** | Powers the ML model |
| **Matplotlib & Seaborn** | Makes the charts look good |
| **HTML/CSS** | The frontend you actually see |

---

## Project Structure

Nothing too complicated — here's how the files are laid out:

```
anomaly-detection/
├── combine_dataset.ipynb          # Notebook to combine & prep your data
├── anomaly_detection_model.pkl    # The trained model (ready to go!)
├── app.py                         # Main Flask app
├── templates/
│   ├── index.html                 # Dashboard page
│   └── test.html                  # Testing page
├── combined_dataset.csv           # Merged dataset
├── cloud_data.csv                 # Sample cloud data
└── README.md                      # You're reading it :)
```

---

## How Does It Actually Work?

Think of it like this:

1. **Gather the data** — We collect cloud metrics like CPU usage, memory, network traffic, disk I/O, etc.
2. **Clean it up** — Raw data is messy. We preprocess it so the model can make sense of it.
3. **Train the model** — An Isolation Forest learns what "normal" looks like by studying the patterns.
4. **Make predictions** — New data comes in, and the model flags anything that looks off (`0` = normal, `-1` = anomaly).
5. **Show the results** — Everything gets plotted on charts and tables so you can see what's happening at a glance.

---

## Getting Started

### Prerequisites

Make sure you have **Python 3.9 or later** installed. Then grab the dependencies:

```bash
pip install Flask pandas scikit-learn matplotlib seaborn numpy
```

That's it — you're good to go.

---

### Option 1: Just Run It (Quickest Way)

We've already included a pre-trained model (`anomaly_detection_model.pkl`), so you can skip the training step entirely.

```bash
cd anomaly-detection
python app.py
```

Then open your browser and head to the address shown in the terminal. Done! 🎉

---

### Option 2: Train Your Own Model

Want to use your own dataset? No problem.

1. Drop your CSV file into the project folder (make sure it has numerical columns).
2. Fire up the notebook:
   ```bash
   jupyter notebook combine_dataset.ipynb
   ```
3. Run through the cells — it'll train a fresh model and save it as `anomaly_detection_model.pkl`.
4. Then just start the Flask app like in Option 1.

---

## Using the Dashboard

Once the app is running, you'll find two main pages:

### 🏠 Home Dashboard
This is where the action is. You'll see:
- **Charts** showing CPU usage, memory, disk usage, and network traffic over time
- A quick **summary** of how many data points are normal vs. anomalous
- A **detailed table** listing every detected anomaly

### 🧪 Test Page
Want to try it yourself? Head to the test page where you can:
- Upload your own CSV file
- Run the model against it
- See the results instantly

---

## What's in the Dataset?

The sample dataset includes these features:

| Feature | Description |
|---------|------------|
| Timestamp | When the data was recorded |
| CPU Usage (%) | How hard the processor is working |
| Memory Usage (%) | RAM consumption |
| Disk I/O (MB/s) | Read/write activity |
| Network In (Mbps) | Incoming traffic |
| Network Out (Mbps) | Outgoing traffic |
| Process Count | Number of running processes |
| Anomaly Score | How "unusual" the data point is |
| Is Anomaly | `0` for normal, `-1` for anomaly |

---

## Questions or Issues?

If something isn't working or you have ideas to improve this, feel free to open an issue or reach out. Happy detecting! 🚀
