# IBB Veri Merkezi

İstanbul Büyükşehir Belediyesi'nin (İBB) Açık Veri Portalı dahilindeki servisler için kolay erişim sağlar.

## Kurulum

```bash
  pip install ibb-veri-merkezi
```
## Kullanım

```python
from ibb_veri_merkezi import get_parking_lots, get_parking_lot

print(get_parking_lots(to_frame=True))
print(get_parking_lot(1487))
```
