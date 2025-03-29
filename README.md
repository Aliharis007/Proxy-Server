# 🌐 **Python Proxy Server**  

A lightweight, multi-threaded HTTP proxy server built with Python. It intercepts and forwards HTTP requests while handling errors efficiently.  

## 🚀 **Features**  

✔️ Supports **GET** requests  
✔️ Multi-processing for handling multiple clients  
✔️ **Error handling** for bad requests and unreachable servers  
✔️ Simple and **easy-to-configure** proxy settings  
✔️ Includes a **test script** for verification  

## 🛠 **Installation & Setup**  

### **Prerequisites**  

Ensure you have **Python 3.x** installed on your system.  

### **1️⃣ Clone the Repository**  

```sh
git clone https://github.com/Aliharis007/Proxy-Server.git
cd Proxy-Server
```

### **2️⃣ Run the Proxy Server**  

```sh
python proxy.py <port>
```

For example, to run it on **port 9090**:  

```sh
python proxy.py 9090
```

### **3️⃣ Test the Proxy**  

A test script is included to verify the proxy functionality. Run:  

```sh
python test_proxy.py
```

## 📂 **Project Structure**  

```
📦 Proxy-Server
├── proxy.py         # Main proxy server script
├── test_proxy.py    # Test script for proxy validation
├── README.md        # Project documentation
└── requirements.txt # Dependencies (if any)
```

## 📜 **Usage**  

- Start the proxy server on a desired port  
- Configure your **browser or application** to use `localhost:<port>` as a proxy  
- The proxy will **forward requests** to the actual web servers and return the responses  

🔹 **Happy Coding!** 😊🚀
