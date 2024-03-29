> please use 'administrator privileges' or 'sudo' to run this script or code.

For more details, also visit <https://toyger-cat.github.io/tech/github.html>

# Why 

Access to GitHub in Chinese mainland is sometimes slow, because DNS is polluted, which leads to the failure of access. Some people say you need to install an accelerator, others say you need to use some magic. But is there a more elegant way to solve it? The answer is: you need to manually parse DNS.

# Code

'main.py' is source code.

'{system}_SCRIPT's are scripts that we package under different operating systems. They are more time-sensitive.

If you find that they are not working, it would be great if you could report an issues. Other suggestions would also be welcome。

# How to Use?

## Use script we provide directly 

```txt
git clone https://github.com/water-pill/resolve-DNS-pollution.git
```

Run {system}_SCRIPT according to your operating system.


## Run source code ( Stable but requires a configuration environment )

```txt
git clone https://github.com/water-pill/resolve-DNS-pollution.git
```

```python
pip install requests beautifulsoup4
```

```python
sudo python3 main.py
```
> ps: Commands may vary slightly depending on the operating system

### Get script locally

```python
pip install pyinstaller
```

```python
pyinstaller --onefile python.py
```

The executable file is in folder <strong>'dist'</strong>. The 'build' folder can be deleted at will.
