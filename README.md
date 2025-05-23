# FuzzyFootballPerformance

# Futbol Takımı Performans Tahmini - Fuzzy Logic Uygulaması

Bu proje, Python dili ve `scikit-fuzzy` kütüphanesi kullanılarak geliştirilmiş, futbol takımı performansını ve beklenen gol sayısını tahmin eden bir **bulanık mantık (fuzzy logic)** tabanlı modeldir. Ayrıca `Tkinter` ile oluşturulmuş kullanıcı dostu bir arayüzü ve matplotlib grafiklerini içermektedir.

---

## İçindekiler
- [Proje Hakkında](#proje-hakkında)
- [Kullanılan Teknolojiler](#kullanılan-teknolojiler)
- [Fuzzy Mantık Modeli](#fuzzy-mantık-modeli)
- [Kullanıcı Arayüzü](#kullanıcı-arayüzü)
- [Kurulum ve Çalıştırma](#kurulum-ve-çalıştırma)
- [Kullanım](#kullanım)
- [Grafikler ve Görselleştirme](#grafikler-ve-görselleştirme)
- [Geliştirme ve Katkı](#geliştirme-ve-katkı)
- [Lisans](#lisans)

---

## Proje Hakkında

Bu uygulama, bir futbol takımının maç performansını ve beklenen gol sayısını tahmin etmek amacıyla aşağıdaki girdileri kullanır:

- Topa Sahiplik (%)  
- Atak Sayısı  
- Savunma Başarı (%)  
- Orta Yüzdesi (%)  
- Motivasyon (1-10 arası)

Bu girdiler fuzzy mantık ile değerlendirilerek maç performansı ve beklenen gol sayısı tahmini yapılır.

---

## Kullanılan Teknolojiler

- Python 3.x  
- [scikit-fuzzy (skfuzzy)](https://pythonhosted.org/scikit-fuzzy/) — Bulanık mantık işlemleri için  
- Tkinter — Grafiksel kullanıcı arayüzü (GUI) için  
- matplotlib — Grafiklerin çizimi için  
- numpy — Sayısal işlemler için

---

## Fuzzy Mantık Modeli

- **Girdi Değişkenleri (Antecedents):**  
  - Topa Sahiplik, Atak Sayısı, Savunma Başarı, Orta Yüzdesi, Motivasyon  
- **Çıktı Değişkenleri (Consequents):**  
  - Maç Performansı, Beklenen Gol  
- **Üyelik Fonksiyonları:**  
  - Her değişken için `kotu`, `orta` ve `iyi` gibi üç bulanık küme tanımlanmıştır.  
- **Kurallar:**  
  - Girdiler arasındaki ilişkiler kurallar ile modellenmiştir. Örneğin:  
    - "Topa sahiplik, atak sayısı ve motivasyon yüksekse maç performansı yüksek olur."  
    - "Savunma başarısı ve orta yüzdesi orta ise maç performansı orta olur."  
    - "Motivasyon veya savunma başarısı kötü ise maç performansı düşük olur."  
- Bu kuralların sonuçları beklenen gol tahminine de etki eder.

---

## Kullanıcı Arayüzü

- Girdi alanları: Kullanıcıdan futbol performans göstergeleri alınır.  
- Hesapla butonu: Girdi verileri ile fuzzy kontrol sistemi çalıştırılır.  
- Sonuç etiketleri: Maç performans tahmini ve beklenen gol sayısı sonucu gösterilir.  
- Notebook ile iki sekme:  
  - **Girdi Grafikleri:** Girdi değişkenlerinin üyelik fonksiyonları ve seçilen değerler kırmızı çizgi ile gösterilir.  
  - **Çıktı Grafikleri:** Tahmin edilen maç performansı ve gol sayısının üyelik fonksiyonları ile birlikte sonuç değerleri grafik üzerinde gösterilir.

---

## Kurulum ve Çalıştırma

1. Python 3.x yüklü olmalıdır.  
2. Gerekli kütüphaneleri yükleyin:

```bash
pip install numpy scikit-fuzzy matplotlib
