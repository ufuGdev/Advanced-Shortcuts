# Advanced Shortcuts
A customizable radial menu for Windows shortcuts and programs, inspired by GTA V's radial menu.

## English

### Features
- Radial menu activated by mouse button (default: Mouse Button 5)
- Customizable shortcuts for programs and keyboard combinations
- Transparent overlay
- Background operation (no taskbar icon)
- Low CPU usage when idle

### Installation
1. Install Python 3.x
2. Install required packages: 

```
pip install pygame keyboard pynput
```

### Configuration
Edit `config.json` to customize your shortcuts.

### Mouse Button Options
- `left`: Left mouse button
- `right`: Right mouse button
- `middle`: Middle mouse button (scroll wheel)
- `xbutton1`: Mouse Button 4 (usually back button)
- `xbutton2`: Mouse Button 5 (usually forward button)

### Usage
1. Run `main.py`
2. Hold the configured mouse button (default: Mouse Button 5) to show the menu
3. Move mouse to select an option
4. Release the button to execute the selected option

### Shortcut Types
- `program`: Launch programs (e.g., chrome.exe)
- `hotkey`: Keyboard shortcuts (e.g., ctrl+shift+esc)

### Common Windows Shortcuts
- `ctrl+shift+esc`: Task Manager
- `windows+l`: Lock PC
- `windows+shift+s`: Screenshot Tool
- `windows+e`: File Explorer
- `windows+r`: Run
- `windows+i`: Settings

---

## Türkçe

### Özellikler
- Fare düğmesiyle aktifleşen radyal menü (varsayılan: Fare Düğmesi 5 (mousenin yanındaki 2 tuştan biri))
- Programlar ve klavye kısayolları için özelleştirilebilir kısayollar
- Şeffaf arayüz
- Arka planda çalışma (görev çubuğunda simge yok)
- Boştayken düşük CPU kullanımı

### Kurulum
1. Python 3.x'i yükleyin
2. Gerekli paketleri yükleyin.
```
pip install pygame keyboard pynput
```

### Yapılandırma
Kısayollarınızı özelleştirmek için `config.json` dosyasını düzenleyin.


### Fare Düğmesi Seçenekleri
- `left`: Sol fare düğmesi
- `right`: Sağ fare düğmesi
- `middle`: Orta fare düğmesi (tekerlek)
- `xbutton1`: Fare Düğmesi 4 (genellikle geri düğmesi)
- `xbutton2`: Fare Düğmesi 5 (genellikle ileri düğmesi)

### Kullanım
1. `main.py` dosyasını çalıştırın
2. Menüyü göstermek için yapılandırılmış fare düğmesini (varsayılan: Fare Düğmesi 5) basılı tutun
3. Seçenek seçmek için fareyi hareket ettirin
4. Seçili seçeneği çalıştırmak için düğmeyi bırakın

### Kısayol Tipleri
- `program`: Program çalıştırma (örn: chrome.exe)
- `hotkey`: Klavye kısayolu (örn: ctrl+shift+esc)

### Sık Kullanılan Windows Kısayolları
- `ctrl+shift+esc`: Görev Yöneticisi
- `windows+l`: Bilgisayarı Kilitle
- `windows+shift+s`: Ekran Alıntısı
- `windows+e`: Dosya Gezgini
- `windows+r`: Çalıştır
- `windows+i`: Ayarlar