# Keçeci Numbers: Keçeci Sayıları

---

## Description / Açıklama

**Keçeci Numbers (Keçeci Sayıları)**: Keçeci Numbers; An Exploration of a Dynamic Sequence Across Diverse Number Sets: This work introduces a novel numerical sequence concept termed "Keçeci Numbers." Keçeci Numbers are a dynamic sequence generated through an iterative process, originating from a specific starting value and an increment value. In each iteration, the increment value is added to the current value, and this "added value" is recorded in the sequence. Subsequently, a division operation is attempted on this "added value," primarily using the divisors 2 and 3, with the choice of divisor depending on the one used in the previous step. If division is successful, the quotient becomes the next element in the sequence. If the division operation fails, the primality of the "added value" (or its real/scalar part for complex/quaternion numbers, or integer part for rational numbers) is checked. If it is prime, an "Augment/Shrink then Check" (ASK) rule is invoked: a type-specific unit value is added or subtracted (based on the previous ASK application), this "modified value" is recorded in the sequence, and the division operation is re-attempted on it. If division fails again, or if the number is not prime, the "added value" (or the "modified value" post-ASK) itself becomes the next element in the sequence. This mechanism is designed to be applicable across various number sets, including positive and negative real numbers, complex numbers, floating-point numbers, rational numbers, and quaternions. The increment value, ASK unit, and divisibility checks are appropriately adapted for each number type. This flexibility of Keçeci Numbers offers rich potential for studying their behavior in different numerical systems. The patterns exhibited by the sequences, their convergence/divergence properties, and potential for chaotic behavior may constitute interesting research avenues for advanced mathematical analysis and number theory applications. This study outlines the fundamental generation mechanism of Keçeci Numbers and their initial behaviors across diverse number sets.

---

## Installation / Kurulum

```bash
conda install bilgi::kececinumbers -y

pip install kececinumbers
```
https://anaconda.org/bilgi/kececinumbers

https://pypi.org/project/kececinumbers/

https://github.com/WhiteSymmetry/kececinumbers

https://zenodo.org/records/

https://zenodo.org/records/

---

## Usage / Kullanım

### Example

```python
import matplotlib.pyplot as plt
import random
import numpy as np
import math
from fractions import Fraction
import quaternion # pip install numpy numpy-quaternion
```

![Keçeci Numbers Example](https://github.com/WhiteSymmetry/kececinumbers/blob/main/examples/kn-1.png?raw=true)

![Keçeci Numbers Example](https://github.com/WhiteSymmetry/kececinumbers/blob/main/examples/kn-2.png?raw=true)

![Keçeci Numbers Example](https://github.com/WhiteSymmetry/kececinumbers/blob/main/examples/kn-3.png?raw=true)

![Keçeci Numbers Example](https://github.com/WhiteSymmetry/kececinumbers/blob/main/examples/kn-4.png?raw=true)

![Keçeci Numbers Example](https://github.com/WhiteSymmetry/kececinumbers/blob/main/examples/kn-5.png?raw=true)

---

## License / Lisans

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Citation

If this library was useful to you in your research, please cite us. Following the [GitHub citation standards](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-on-github/about-citation-files), here is the recommended citation.

### BibTeX

```bibtex
@misc{kececi_2025_15313947,
  author       = {Keçeci, Mehmet},
  title        = {kececinumbers},
  month        = may,
  year         = 2025,
  publisher    = {PyPI, Anaconda, Github, Zenodo},
  version      = {0.1.0},
  doi          = {10.5281/zenodo.},
  url          = {https://doi.org/10.5281/zenodo.},
}

@misc{kececi_2025_15314329,
  author       = {Keçeci, Mehmet},
  title        = {Keçeci numbers},
  month        = may,
  year         = 2025,
  publisher    = {Zenodo},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.},
  url          = {https://doi.org/10.5281/zenodo.},
}
```

### APA

```
Keçeci, M. (2025). kececinumbers (0.1.0). PyPI, Anaconda, GitHub, Zenodo. https://doi.org/10.5281/zenodo.

Keçeci, M. (2025). Keçeci Numbers. https://doi.org/10.5281/zenodo.
```

### Chicago
```
Keçeci, Mehmet. "kececinumbers". PyPI, Anaconda, GitHub, Zenodo, 01 May 2025. https://doi.org/10.5281/zenodo.

Keçeci, Mehmet. "Keçeci Numbers", 01 May 2025. https://doi.org/10.5281/zenodo.
```
