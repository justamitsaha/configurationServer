import re

# ---- read java file ----
with open("input.java", "r", encoding="utf-8") as f:
    code = f.read()

# ---- regex to capture keys passed to baseProfile.setProperty("KEY", ...) ----
pattern = r'baseProfile\.setProperty\s*\(\s*"([^"]+)"'

# ---- find all keys ----
keys = re.findall(pattern, code)

# ---- remove duplicates while preserving order ----
seen = set()
unique_keys = []
for k in keys:
    if k not in seen:
        seen.add(k)
        unique_keys.append(k)

# ---- print comma separated ----
print(",".join(unique_keys))
