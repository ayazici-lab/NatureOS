
import csv
import io
import os
import re
import unicodedata

import streamlit as st

NATUREOS_VERSION = "2.2.2"

st.set_page_config(
    page_title=f"NatureOS {NATUREOS_VERSION}",
    page_icon="🌿",
    layout="wide"
)

st.title(f"🌿 NatureOS {NATUREOS_VERSION}")
st.markdown("**Ayşe Meriç Yazıcı**")
st.subheader("Nature-Inspired Innovation Engine")

st.write(
    "Doğanın biyolojik mekanizmalarından "
    "ilham alan inovasyon ve problem çözme platformu."
)

st.divider()

# Biyolojik bilgi tabanı
biological_database = [
    {
        "keywords": ["enerji", "havalandırma", "ısı"],
        "organism": "Termit yuvaları",
        "mechanism": "Pasif havalandırma ve sıcaklık düzenleme",
        "solution": "Enerji tasarruflu bina havalandırma sistemi",
        "explanation": (
            "Bazı termit yuvalarındaki hava akışı ve "
            "ısı düzenleme mekanizmaları, "
            "düşük enerjili bina tasarımlarına ilham verebilir."
        )
    },
    {
        "keywords": ["su", "nem", "kuraklık"],
        "organism": "Namib çöl böceği",
        "mechanism": "Yüzey özellikleriyle nem toplama",
        "solution": "Atmosferik su toplama yüzeyi",
        "explanation": (
            "Çöl böceklerinin yüzey yapıları, "
            "havadaki nemin toplanmasına yönelik "
            "malzeme tasarımlarına ilham verebilir."
        )
    },
    {
        "keywords": ["dayanıklılık", "malzeme", "hafif"],
        "organism": "Örümcek ipeği",
        "mechanism": "Hafif ve dayanıklı lif yapısı",
        "solution": "Biyomimetik kompozit malzeme",
        "explanation": (
            "Örümcek ipeğinin mekanik özellikleri, "
            "hafif ve dayanıklı malzeme geliştirme "
            "çalışmalarına örnek olabilir."
        )
    },
    {
        "keywords": ["soğutma", "sıcaklık", "serinletme"],
        "organism": "Termit yuvaları",
        "mechanism": "Pasif ısı yönetimi",
        "solution": "Biyomimetik pasif soğutma sistemi",
        "explanation": (
            "Doğal hava akışı ve ısı transferi "
            "ilkeleri kullanılarak soğutma "
            "ihtiyacı azaltılabilir."
        )
    },
    {
        "keywords": ["yapışma", "yapıştırıcı", "tutunma"],
        "organism": "Geko kertenkelesi",
        "mechanism": "Mikroskobik yüzey etkileşimleri",
        "solution": "Tekrar kullanılabilir kuru yapışkan yüzey",
        "explanation": (
            "Gekoların ayak yapıları, "
            "kimyasal yapıştırıcı gerektirmeyen "
            "yüzey teknolojilerine ilham verir."
        )
    },
    {
        "keywords": ["temizlik", "kir", "yüzey"],
        "organism": "Lotus yaprağı",
        "mechanism": "Süperhidrofobik yüzey yapısı",
        "solution": "Kendini temizleyen kaplama",
        "explanation": (
            "Lotus yaprağının yüzey yapısı, "
            "su damlacıklarının kirleri uzaklaştırdığı "
            "kaplamalara ilham verebilir."
        )
    },
    {
        "keywords": ["uçuş", "kanat", "aerodinamik"],
        "organism": "Kuş kanatları",
        "mechanism": "Aerodinamik kaldırma ve akış kontrolü",
        "solution": "Verimli kanat geometrisi",
        "explanation": (
            "Kuşların kanat geometrileri, "
            "hava araçlarında aerodinamik "
            "verimlilik çalışmalarına ilham verebilir."
        )
    },
    
    {
        "keywords": [
            "sürtünme",
            "akış",
            "direnç",
            "gemi",
            "hidrodinamik"
        ],
        "organism": "Köpekbalığı derisi",
        "mechanism": (
            "Mikroskobik yüzey olukları ve "
            "akışkan-yüzey etkileşimleri"
        ),
        "solution": (
            "Akış direncini azaltmaya yönelik "
            "biyomimetik yüzey kaplaması"
        ),
        "explanation": (
            "Köpekbalığı derisindeki bazı "
            "mikroskobik yapılar, uygun akış "
            "koşullarında sürtünme direncinin "
            "azaltılmasına ilham verebilir."
        )
    },
    
    {
        "keywords": [
            "nem",
            "kozalak",
            "cephe",
            "havalandırma",
            "açılma",
            "kapanma"
        ],
        "organism": "Çam kozalağı",
        "mechanism": "Kozalak pullarının nem değişimine bağlı higromorfik hareketi",
        "solution": "Neme duyarlı, pasif hareket eden biyomimetik yapı elemanları",
        "explanation": "Çam kozalağı pullarındaki farklı doku katmanları nem değişimlerine farklı tepkiler verir. Bu özellik, dış enerji gerektirmeden şekil değiştirebilen yapı ve malzeme tasarımlarına ilham verebilir."
    },

    {
        "keywords": [
            "kanat",
            "türbin",
            "pervane",
            "kaldırma",
            "aerodinamik",
            "verimlilik"
        ],
        "organism": "Kambur balina",
        "mechanism": (
            "Göğüs yüzgeçlerinin ön kenarındaki "
            "tüberküllerin akış davranışını etkilemesi"
        ),
        "solution": (
            "Kanat, pervane ve türbin tasarımlarında "
            "biyomimetik ön kenar geometrileri"
        ),
        "explanation": (
            "Kambur balinanın göğüs yüzgeçlerindeki "
            "çıkıntılar, belirli koşullarda akış "
            "ayrılmasını geciktirebilir ve kaldırma "
            "performansını etkileyebilir. Bu özellik "
            "aerodinamik tasarımlara ilham verebilir."
        )
    },

    {
        "keywords": [
            "gürültü",
            "ses",
            "sessiz",
            "fan",
            "pervane",
            "titreşim"
        ],
        "organism": "Baykuş kanadı",
        "mechanism": (
            "Kanat tüylerinin kenar ve yüzey "
            "yapılarının aerodinamik sesi azaltması"
        ),
        "solution": (
            "Fan, pervane ve türbinlerde "
            "biyomimetik gürültü azaltma tasarımları"
        ),
        "explanation": (
            "Baykuşların kanat tüylerindeki "
            "taraksı ön kenarlar, saçaklı arka "
            "kenarlar ve yüzey özellikleri "
            "hava akışından kaynaklanan sesin "
            "azaltılmasına katkıda bulunabilir. "
            "Bu mekanizmalar sessiz çalışan "
            "aerodinamik sistemlere ilham verir."
        )
    },

    {
        "keywords": [
            "sis",
            "damla",
            "yoğuşma",
            "su",
            "toplama",
            "kuraklık"
        ],
        "organism": "Kaktüs dikenleri",
        "mechanism": (
            "Diken geometrisi ve yüzey özellikleriyle "
            "su damlacıklarının toplanması ve taşınması"
        ),
        "solution": (
            "Sis ve havadaki nemden su toplamaya "
            "yönelik biyomimetik yüzey sistemleri"
        ),
        "explanation": (
            "Bazı kaktüs türlerinde dikenlerin "
            "konik geometrisi ve yüzey özellikleri, "
            "sis damlacıklarının yakalanmasını "
            "ve yönlendirilmesini destekleyebilir. "
            "Bu mekanizma, düşük enerji gerektiren "
            "su toplama tasarımlarına ilham verebilir."
        )
    },

    {
        "keywords": [
            "renk",
            "pigment",
            "optik",
            "ışık",
            "yansıma",
            "sensör"
        ],
        "organism": "Morpho kelebeği",
        "mechanism": (
            "Kanat pullarındaki mikroskobik "
            "yapıların ışıkla etkileşerek "
            "yapısal renk oluşturması"
        ),
        "solution": (
            "Yapısal renkli biyomimetik kaplamalar, "
            "optik sensörler ve güvenlik etiketleri"
        ),
        "explanation": (
            "Morpho kelebeğinin kanat pullarındaki "
            "mikroskobik yapılar ışığın yansımasını "
            "ve girişimini etkiler. Bu özellik, "
            "bazı uygulamalarda pigment kullanımını "
            "azaltabilecek yapısal renk sistemlerine "
            "ve optik teknolojilere ilham verebilir."
        )
    },

    {
        "keywords": [
            "yapışma",
            "yapıştırıcı",
            "su",
            "ıslak",
            "tutunma",
            "biyomalzeme"
        ],
        "organism": "Deniz midyesi",
        "mechanism": (
            "Byssus lifleri ve özel proteinler "
            "aracılığıyla ıslak yüzeylere tutunma"
        ),
        "solution": (
            "Su altında kullanılabilen biyomimetik "
            "yapıştırıcılar ve biyouyumlu kaplamalar"
        ),
        "explanation": (
            "Deniz midyelerinin tutunma sistemlerinde "
            "özel proteinler ve kimyasal etkileşimler "
            "rol oynar. Bu mekanizmalar, ıslak "
            "ortamlarda çalışabilen yapıştırıcıların "
            "ve biyomalzemelerin geliştirilmesine "
            "ilham verebilir."
        )
    },

    {
        "keywords": [
            "darbe",
            "çatlak",
            "kırılma",
            "kompozit",
            "dayanıklılık",
            "koruma"
        ],
        "organism": "Abalon deniz kabuğu",
        "mechanism": (
            "Sedef tabakasındaki sert mineral "
            "levhacıkların ve organik katmanların "
            "çok katmanlı düzeni"
        ),
        "solution": (
            "Darbeye ve çatlak ilerlemesine karşı "
            "dayanıklı biyomimetik kompozit malzemeler"
        ),
        "explanation": (
            "Abalon kabuğunun sedef tabakasındaki "
            "mineral levhacıklar ve organik ara "
            "katmanlar, çatlakların ilerlemesini "
            "zorlaştırabilir ve enerjinin dağıtılmasına "
            "katkıda bulunabilir. Bu yapı, dayanıklı "
            "kompozit tasarımlarına ilham verebilir."
        )
    },

    {
        "keywords": [
            "lojistik",
            "rota",
            "optimizasyon",
            "dağıtım",
            "tedarik",
            "taşıma"
        ],
        "organism": "Karınca kolonileri",
        "mechanism": (
            "Feromon izleri ve yerel etkileşimlerle "
            "kolektif rota seçimi ve kaynak arama"
        ),
        "solution": (
            "Karınca kolonisi optimizasyonundan "
            "ilham alan lojistik ve dağıtım "
            "rotası planlama sistemleri"
        ),
        "explanation": (
            "Karıncalar, feromon izleri ve çevresel "
            "geri bildirimler aracılığıyla "
            "alternatif yollar arasında kolektif "
            "seçimler yapabilir. Bu davranış, "
            "karınca kolonisi optimizasyonu "
            "algoritmalarına ilham vermiştir. "
            "Bu algoritmalar lojistik, rota "
            "planlama ve kaynak tahsisi "
            "problemlerinde kullanılabilir."
        )
    },

    {
        "keywords": [
            "karar",
            "ekip",
            "koordinasyon",
            "kolektif",
            "uzlaşma",
            "organizasyon"
        ],
        "organism": "Bal arısı kolonileri",
        "mechanism": (
            "Keşifçi arıların bilgi paylaşımı "
            "ve kolektif değerlendirme yoluyla "
            "yuva yeri seçimi"
        ),
        "solution": (
            "Kolektif zekadan ilham alan "
            "dağıtık karar destek ve "
            "ekip koordinasyon sistemleri"
        ),
        "explanation": (
            "Bal arıları yeni yuva ararken "
            "keşifçi bireyler alternatif yerleri "
            "değerlendirir ve sallanma dansıyla "
            "bilgi paylaşır. Koloni, bu etkileşimler "
            "sonucunda ortak bir seçime ulaşabilir. "
            "Bu mekanizma, organizasyonlarda "
            "dağıtık karar alma ve kolektif "
            "değerlendirme sistemlerine "
            "ilham verebilir."
        )
    },

    {
        "keywords": [
            "ağ",
            "dayanıklılık",
            "esneklik",
            "kaynak",
            "bağlantı",
            "kriz"
        ],
        "organism": "Mantar miselyum ağları",
        "mechanism": (
            "Dallanıp birleşebilen hif ağları "
            "aracılığıyla kaynaklara erişim "
            "ve çevresel koşullara uyum"
        ),
        "solution": (
            "Esnek organizasyon ağları, "
            "alternatif bağlantılar ve "
            "dayanıklı kaynak paylaşım sistemleri"
        ),
        "explanation": (
            "Mantar miselyumu, çevresine yayılan "
            "hiflerden oluşan bir ağdır. "
            "Bu ağın dallanma ve bağlantı "
            "özellikleri, kaynaklara erişim "
            "ve değişen koşullara uyum "
            "açısından incelenebilir. "
            "Bu özellikler işletmelerde "
            "esnek organizasyon yapıları "
            "ve dayanıklı tedarik ağlarının "
            "tasarımına ilham verebilir."
        )
    },

    {
        "keywords": [
            "işbölümü",
            "görev",
            "örgütlenme",
            "koordinasyon",
            "süreç",
            "organizasyon"
        ],
        "organism": "Termit kolonileri",
        "mechanism": (
            "Yerel etkileşimler ve stigmerji "
            "aracılığıyla kolektif görev "
            "koordinasyonu"
        ),
        "solution": (
            "Merkezi olmayan görev dağılımı, "
            "uyarlanabilir iş akışları ve "
            "öz örgütlenmeye dayalı "
            "organizasyon tasarımları"
        ),
        "explanation": (
            "Termit kolonilerinde bireyler, "
            "çevresel ipuçları ve birbirlerinin "
            "faaliyetlerinin bıraktığı izler "
            "üzerinden davranışlarını "
            "koordine edebilir. Stigmerji "
            "olarak bilinen bu mekanizma, "
            "işletmelerde merkezi olmayan "
            "görev koordinasyonu ve esnek "
            "süreç tasarımlarına ilham verebilir."
        )
    },

    {
        "keywords": [
            "çeviklik",
            "uyum",
            "koordinasyon",
            "hareket",
            "dinamik",
            "ekip"
        ],
        "organism": "Balık sürüleri",
        "mechanism": (
            "Yerel etkileşimler, hizalanma ve "
            "mesafe koruma yoluyla "
            "kolektif hareket"
        ),
        "solution": (
            "Çevik ekip koordinasyonu, "
            "dağıtık karar alma ve "
            "çok etmenli sistem tasarımları"
        ),
        "explanation": (
            "Balık sürülerinde bireyler "
            "yakın çevrelerindeki diğer "
            "balıkların hareketlerine tepki "
            "vererek yön ve hızlarını "
            "uyarlayabilir. Bu yerel "
            "etkileşimlerden kolektif "
            "hareket örüntüleri ortaya çıkar. "
            "Bu mekanizma, organizasyonlarda "
            "çevik ekip koordinasyonuna ve "
            "çok etmenli yapay zeka "
            "sistemlerine ilham verebilir."
        )
    },

    {
        "keywords": [
            "özerklik",
            "dağıtık",
            "zekâ",
            "karar",
            "adaptasyon",
            "robotik"
        ],
        "organism": "Ahtapot",
        "mechanism": (
            "Merkezi sinir sistemiyle etkileşim "
            "içinde çalışan dağıtık sinir ağları "
            "ve yerel motor kontrol"
        ),
        "solution": (
            "Dağıtık yapay zeka sistemleri, "
            "özerk ekip yapıları ve "
            "adaptif robotik kontrol"
        ),
        "explanation": (
            "Ahtapotların sinir sistemindeki "
            "nöronların önemli bir bölümü "
            "kollarında bulunur. Kollar, "
            "merkezi beyinle bağlantılı olarak "
            "yerel duyusal ve motor işlemleri "
            "gerçekleştirebilir. Bu özellik, "
            "dağıtık kontrol mimarilerine, "
            "özerk ekip koordinasyonuna ve "
            "adaptif problem çözme "
            "sistemlerine ilham verebilir."
        )
    },

    {
        "keywords": [
            "ekosistem",
            "kaynak",
            "sürdürülebilirlik",
            "çevre",
            "su",
            "dayanıklılık"
        ],
        "organism": "Kunduzlar",
        "mechanism": (
            "Baraj inşası yoluyla su akışının "
            "ve yerel habitat koşullarının "
            "değiştirilmesi"
        ),
        "solution": (
            "Ekosistem temelli kaynak yönetimi, "
            "sürdürülebilir altyapı ve "
            "çevresel dayanıklılık stratejileri"
        ),
        "explanation": (
            "Kunduzlar akarsular üzerinde "
            "barajlar oluşturarak suyun "
            "hareketini ve çevresel koşulları "
            "değiştirebilir. Bu faaliyetler "
            "bazı bölgelerde sulak alanların "
            "oluşmasına ve habitat "
            "çeşitliliğine katkı sağlayabilir. "
            "Bu mekanizma, işletmelerde "
            "ekosistem temelli stratejilere "
            "ve sürdürülebilir kaynak "
            "yönetimine ilham verebilir."
        )
    },

    {
        "keywords": [
            "çeşitlilik",
            "risk",
            "dayanıklılık",
            "strateji",
            "tedarik",
            "esneklik"
        ],
        "organism": "Orman ekosistemleri",
        "mechanism": (
            "Tür ve işlev çeşitliliği ile "
            "ekolojik etkileşimlerin "
            "ekosistem süreçlerini desteklemesi"
        ),
        "solution": (
            "Stratejik çeşitlendirme, "
            "alternatif tedarik ağları ve "
            "organizasyonel dayanıklılık tasarımları"
        ),
        "explanation": (
            "Orman ekosistemlerinde farklı "
            "türler ve işlevsel gruplar "
            "birlikte bulunur. Belirli koşullarda "
            "işlevsel çeşitlilik, ekosistemin "
            "bazı değişimlere karşı "
            "dayanıklılığını destekleyebilir. "
            "Bu özellik, işletmelerde "
            "risk dağıtımı, tedarikçi "
            "çeşitlendirmesi ve esnek "
            "strateji geliştirme süreçlerine "
            "ilham verebilir."
        )
    },

    {
        "keywords": [
            "işbirliği",
            "ekip",
            "koordinasyon",
            "verimlilik",
            "rotasyon",
            "enerji"
        ],
        "organism": "Göçmen kuşların V uçuş düzeni",
        "mechanism": (
            "V şeklindeki uçuş düzeninde "
            "aerodinamik etkileşimlerden "
            "yararlanılması"
        ),
        "solution": (
            "Ekip iş birliği, görev rotasyonu "
            "ve koordineli kaynak kullanımı "
            "için biyomimetik organizasyon tasarımları"
        ),
        "explanation": (
            "Bazı göçmen kuşlar V şeklinde "
            "uçarak diğer kuşların oluşturduğu "
            "hava akımlarından yararlanabilir. "
            "Bu düzen belirli koşullarda "
            "enerji maliyetini azaltabilir. "
            "Mekanizma, işletmelerde ekip "
            "koordinasyonu, ortak kaynak "
            "kullanımı ve operasyonel "
            "verimlilik tasarımlarına "
            "ilham verebilir."
        )
    },

    {
        "keywords": [
            "lojistik",
            "rota",
            "optimizasyon",
            "tedarik",
            "dağıtım",
            "ulaşım"
        ],
        "organism": "Physarum polycephalum",
        "mechanism": (
            "Besin kaynakları arasında "
            "dallanabilen ve çevresel "
            "koşullara göre yeniden "
            "düzenlenebilen ağ oluşumu"
        ),
        "solution": (
            "Biyomimetik rota optimizasyonu, "
            "lojistik ağ tasarımı ve "
            "uyarlanabilir dağıtım sistemleri"
        ),
        "explanation": (
            "Physarum polycephalum, besin "
            "kaynaklarına ulaşırken tüp "
            "benzeri bağlantılardan oluşan "
            "ağlar geliştirebilir. "
            "Bu bağlantılar kullanım ve "
            "çevresel koşullara bağlı olarak "
            "yeniden düzenlenebilir. "
            "Bu mekanizmadan esinlenen "
            "hesaplama yaklaşımları, "
            "lojistik ağların ve dağıtım "
            "rotalarının tasarımında "
            "değerlendirilebilir."
        )
    },

    {
        "keywords": [
            "kaynak",
            "büyüme",
            "adaptasyon",
            "fırsat",
            "strateji",
            "yatırım"
        ],
        "organism": "Ağaç kök sistemleri",
        "mechanism": (
            "Su ve besin maddelerinin "
            "dağılımına duyarlı kök büyümesi "
            "ve dallanma düzeninin değişmesi"
        ),
        "solution": (
            "Adaptif kaynak tahsisi, "
            "stratejik büyüme planlaması "
            "ve fırsat odaklı yatırım "
            "önceliklendirmesi"
        ),
        "explanation": (
            "Ağaç kökleri topraktaki su "
            "ve besin maddelerinin "
            "dağılımına tepki vererek "
            "büyüme ve dallanma "
            "örüntülerini değiştirebilir. "
            "Bu mekanizma, işletmelerde "
            "kaynakların değişen fırsatlara "
            "göre yönlendirilmesine, "
            "stratejik yatırım kararlarına "
            "ve adaptif büyüme "
            "yaklaşımlarına ilham verebilir."
        )
    },


]


biological_database.extend([{'organism': 'Deniz hıyarının değişken sertlikteki dokusu',
  'keywords': ['ürünü eziyor',
               'ürün eziliyor',
               'cam parçalar kırılıyor',
               'tutucu gevşek kalıyor',
               'hassas parçayı kavrama'],
  'mechanism': 'Bağ dokusunun mekanik sertliğini geri dönüşümlü olarak değiştirmesi.',
  'solution': 'Parçayı sararken esneyen ve taşıma sırasında sertleşen bir robot tutucu tasarımı.',
  'explanation': 'Deniz hıyarının bağ dokusu, sinir sistemi kontrolünde mekanik özelliklerini '
                 'değiştirebilir.',
  'pilot_test': 'Aynı parça ve taşıma hızında sabit sertlikteki tutucuyla değişken sertlikli '
                'prototipi karşılaştırın. Ezilme ve düşme oranlarını ölçün.'},
 {'organism': 'Erodium tohumunun kendini toprağa yerleştirmesi',
  'keywords': ['tohumlar yüzeyde kalıyor',
               'tohumlar toprağa girmiyor',
               'tohumlar rüzgârla dağılıyor',
               'tohumlar rüzgarla dağılıyor',
               'havadan ekim'],
  'mechanism': 'Nem değişimiyle hareket eden tohum uzantısının tohumu toprağa doğru ilerletmesi.',
  'solution': 'Nem değişimiyle çalışan, kendini toprağa yerleştirebilen bir tohum taşıyıcısı.',
  'explanation': "Erodium'un tohum uzantısından esinlenen bir çalışmada kendini toprağa "
                 'yerleştirebilen ahşap bir taşıyıcı geliştirildi.',
  'pilot_test': 'Aynı toprak ve nem döngüsünde çıplak tohum ile taşıyıcılı tohumu karşılaştırın. '
                'Yerleşme oranını ve derinliğini ölçün.'},
 {'organism': 'Hagfish’in suyla temas edince açılan lifleri',
  'keywords': ['tanktan sızıntı',
               'su gidere ulaşıyor',
               'su kaçağı yayılıyor',
               'sızıntı yayılıyor',
               'su döküntüsünü sınırlama'],
  'mechanism': 'Deniz suyuna salınan sıkı lif demetlerinin hızla açılarak müsinle birlikte ağ '
               'oluşturması.',
  'solution': 'Suya temas ettiğinde açılan ve akışı yavaşlatmayı amaçlayan lifli bariyer '
              'prototipi.',
  'explanation': 'Hagfish’in savunma salgısındaki lif demetleri ve müsin, deniz suyunda hızla '
                 'açılıp lifli bir yapı oluşturur.',
  'pilot_test': 'Tezgâh ölçeğinde temiz suyla deneyin. Bariyerin açılma süresini ve sabit sürede '
                'bariyeri geçen su hacmini ölçün.'}])


# NATUREOS 2.1 - PROBLEM KATEGORILERI

scientific_evidence = {
    "Physarum polycephalum": {
        "authors": "Tero et al.",
        "year": 2010,
        "journal": "Science",
        "title": (
            "Rules for biologically inspired "
            "adaptive network design"
        ),
        "doi": "10.1126/science.1177894",
        "biological_evidence": True,
        "technical_validation": True,
        "business_validation": False,
        "note": (
            "Biyolojik ag olusumu ve "
            "matematiksel ag modeli "
            "arastirilmistir. Isletme "
            "uygulamasi bu kaynakla "
            "dogrulanmamistir."
        )
    },
    "Ağaç kök sistemleri": {
        "authors": "Hodge",
        "year": 2004,
        "journal": "New Phytologist",
        "title": (
            "The plastic plant: root responses "
            "to heterogeneous supplies "
            "of nutrients"
        ),
        "doi": (
            "10.1111/j.1469-8137."
            "2004.01015.x"
        ),
        "biological_evidence": True,
        "technical_validation": False,
        "business_validation": False,
        "note": (
            "Koklerin besin dagilimina "
            "verdigi tepkiler literaturde "
            "incelenmistir. Isletme "
            "uygulamasi bir tasarim "
            "onerisidir."
        )
    },

    "Karınca kolonileri": {
        "authors": "Dorigo, Maniezzo & Colorni",
        "year": 1996,
        "journal": (
            "IEEE Transactions on Systems, "
            "Man, and Cybernetics, Part B"
        ),
        "title": (
            "Ant System: Optimization by a "
            "Colony of Cooperating Agents"
        ),
        "doi": "10.1109/3477.484436",
        "biological_evidence": True,
        "technical_validation": True,
        "business_validation": False,
        "note": (
            "Karinca kolonilerinden esinlenen "
            "Ant System optimizasyon algoritmasi "
            "bilimsel olarak tanitilmistir. "
            "Bu makale belirli bir isletmede "
            "uygulama basarisini dogrulamaz."
        )
    }
}

scientific_evidence.update({'Deniz hıyarının değişken sertlikteki dokusu': {'title': 'Mutable Collagenous Tissue: A Concept '
                                                          'Generator for Biomimetic Materials and '
                                                          'Devices',
                                                 'authors': 'Candia Carnevali ve ark.',
                                                 'year': 2024,
                                                 'journal': 'Marine Drugs',
                                                 'doi': '10.3390/md22010037',
                                                 'biological_evidence': True,
                                                 'technical_validation': False,
                                                 'business_validation': False,
                                                 'note': 'Derleme biyolojik mekanizmayı ve '
                                                         'biyomimetik çalışmaları ele alır. Bu '
                                                         'karttaki robot tutucu ayrı bir tasarım '
                                                         'önerisidir.'},
 'Erodium tohumunun kendini toprağa yerleştirmesi': {'title': 'Autonomous self-burying seed '
                                                              'carriers for aerial seeding',
                                                     'authors': 'Luo ve ark.',
                                                     'year': 2023,
                                                     'journal': 'Nature',
                                                     'doi': '10.1038/s41586-022-05656-3',
                                                     'biological_evidence': True,
                                                     'technical_validation': True,
                                                     'business_validation': False,
                                                     'note': 'Araştırma bir tohum taşıyıcı '
                                                             'prototipini inceler. İşletme '
                                                             'koşullarındaki performans ayrıca '
                                                             'değerlendirilmeli.'},
 'Hagfish’in suyla temas edince açılan lifleri': {'title': 'Deployment of hagfish slime thread '
                                                           'skeins requires the transmission of '
                                                           'mixing forces via mucin strands',
                                                  'authors': 'Winegard ve Fudge',
                                                  'year': 2010,
                                                  'journal': 'Journal of Experimental Biology',
                                                  'doi': '10.1242/jeb.038075',
                                                  'biological_evidence': True,
                                                  'technical_validation': False,
                                                  'business_validation': False,
                                                  'note': 'Çalışma liflerin biyolojik açılma '
                                                          'mekanizmasını inceler. Sızıntı bariyeri '
                                                          'test edilecek bir tasarım önerisidir.'}})


# Kaynaklı biyolojik mekanizmalar ve işletme senaryoları.
model_catalog = [
    {
        "organism": 'Peygamberdevesi karidesinin darbe sopası',
        "category": 'Malzeme ve Darbe Dayanımı',
        "keywords": [
            'darbe uçları çatlıyor',
            'tekrarlı darbede kırılıyor',
            'darbe altında katmanlar ayrılıyor',
        ],
        "mechanism": 'Darbe bölgesinin altındaki spiral lif katmanları çatlakların ilerlediği yolu değiştirir.',
        "solution": 'Aşınan darbe uçları için farklı açılarda istiflenen lifli katmanlardan bir prototip.',
        "pilot_test": 'Aynı kütlede iki numuneye tekrarlı darbe uygulayıp ilk çatlağa kadar çevrim sayısını ölçün.',
        "source_title": 'The stomatopod dactyl club: a formidable damage-tolerant biological hammer',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/22679090/',
        "technical_validation": False,
    },
    {
        "organism": 'Derin deniz cam süngerinin çapraz kafesi',
        "category": 'Hafif Yapılar ve Yapısal Tasarım',
        "keywords": [
            'kafes yapı burkuluyor',
            'hafif taşıyıcı eziliyor',
            'çapraz destek tasarlamak',
        ],
        "mechanism": 'Euplectella süngerinin kare iskelet hücreleri çift diyagonal desteklerle takviye edilir.',
        "solution": 'Aynı malzeme miktarında çift diyagonalli hafif taşıyıcı kafes.',
        "pilot_test": 'Aynı kütlede düz ve çift diyagonalli kafesleri sıkıştırıp burkulma yükünü karşılaştırın.',
        "source_title": 'Mechanically robust lattices inspired by deep-sea glass sponges',
        "source_url": 'https://www.nature.com/articles/s41563-020-0798-1',
        "technical_validation": True,
    },
    {
        "organism": 'Deniz tarağının kristal aynaları',
        "category": 'Optik ve Görüntüleme',
        "keywords": [
            'kamera karanlıkta zorlanıyor',
            'minyatür optik tasarlıyoruz',
            'mercek yerine ayna',
        ],
        "mechanism": 'Deniz tarağı gözünde katmanlı guanin kristallerinden oluşan ayna ışığı retinaya yansıtır.',
        "solution": 'Sığ bir sensör gövdesi için çok katmanlı yansıtıcı optik düzenek.',
        "pilot_test": 'Aynı gövde derinliğinde görüntü parlaklığını ve görüş alanındaki çözünürlüğü ölçün.',
        "source_title": 'The image-forming mirror in the eye of the scallop',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/29191905/',
        "technical_validation": False,
    },
    {
        "organism": 'Bombardıman böceğinin darbeli püskürtmesi',
        "category": 'Akış ve Dozaj',
        "keywords": [
            'nozul tek seferde fazla püskürtüyor',
            'sıvıyı darbeli vermek',
            'aralıklı mikro dozlama',
        ],
        "mechanism": 'Savunma odasındaki basınç değişimi giriş vanasının kapanıp açılmasını sağlayarak darbeli püskürtme oluşturur.',
        "solution": 'Kimyasal reaksiyon kullanmadan basınç geri beslemesiyle aralıklı doz veren bir vana.',
        "pilot_test": 'Su ile sabit basınçta deneme yapın. Doz başına hacmi ve çevrimler arası sapmayı ölçün.',
        "source_title": 'Mechanistic origins of bombardier beetle explosion-induced defensive spray pulsation',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/25931557/',
        "technical_validation": False,
    },
    {
        "organism": 'Su yüzeyi böceğinin bölünmüş gözleri',
        "category": 'Optik ve Görüntüleme',
        "keywords": [
            'kamera suyun altını ve üstünü',
            'su seviyesinin iki tarafı',
            'su üstü ve su altı görüntüsü',
        ],
        "mechanism": 'Gyrinidae böceklerinin bölünmüş gözleri suyun altını ve üstünü aynı anda izlemeye olanak verir.',
        "solution": 'Bir su seviyesi hattının iki tarafını izleyen ayrı optik pencereli kamera muhafazası.',
        "pilot_test": 'Dalgalı su yüzeyinde eşzamanlı görünür alanı ve okunabilen hedef sayısını karşılaştırın.',
        "source_title": 'Whirligig Beetle',
        "source_url": 'https://australian.museum/learn/animals/insects/whirligig-beetle/',
        "technical_validation": False,
    },
    {
        "organism": 'Salvinia eğreltisinin hava tutan tüyleri',
        "category": 'Islak Yüzeyler ve Akış',
        "keywords": [
            'sualtında hava tabakası',
            'hava filmi kayboluyor',
            'hava tabakasını korumak',
        ],
        "mechanism": 'Su itici tüylerin su seven uçları hava-su ara yüzünün sabitlenmesine katkıda bulunur.',
        "solution": 'Su altında hava filmi tutmayı amaçlayan uçları farklı ıslanabilirlikte bir yüzey.',
        "pilot_test": 'Şeffaf su tankında hava tabakasının kalma süresini ve basınç değişimine tepkisini ölçün.',
        "source_title": 'The Salvinia Paradox: Superhydrophobic Surfaces with Hydrophilic Pins for Air Retention Under Water',
        "source_url": 'https://doi.org/10.1002/adma.200904411',
        "technical_validation": False,
    },
    {
        "organism": 'Venüs sinekkapanının temas sayacı',
        "category": 'Sensörler ve Otomasyon',
        "keywords": [
            'tek dokunuşta yanlış tetikleniyor',
            'yanlış alarm veriyor',
            'iki temasla çalışsın',
        ],
        "mechanism": 'Dionaea muscipula kapanı, tetik tüylerinden gelen elektriksel olayların sayısına göre farklı tepkiler üretir.',
        "solution": 'Tek seferlik parazitleri süzen, belirli aralıkta birden fazla sinyal bekleyen bir sensör mantığı.',
        "pilot_test": 'Kayıtlı sensör verisiyle yanlış alarm ve kaçırılan gerçek olay oranlarını birlikte ölçün.',
        "source_title": 'The Venus Flytrap Dionaea muscipula Counts Prey-Induced Action Potentials to Induce Sodium Uptake',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/26804557/',
        "technical_validation": False,
    },
    {
        "organism": 'Buz çiçeğinin suyla açılan kapsülü',
        "category": 'Tarım ve Pasif Mekanizmalar',
        "keywords": [
            'yağmurda kapak açılsın',
            'ıslanınca açılan kapak',
            'suyla kendiliğinden açılması',
        ],
        "mechanism": 'Tohum kapsülündeki şişebilen doku ıslandığında katlanmış yapının açılmasını sağlar.',
        "solution": 'Elektrik gerektirmeyen ve suyla açılan bir numune toplama kapağı.',
        "pilot_test": 'Tekrarlı ıslanma ve kuruma çevrimlerinde açılma açısını ve açılma süresini ölçün.',
        "source_title": 'Origami-like unfolding of hydro-actuated ice plant seed capsules',
        "source_url": 'https://www.nature.com/articles/ncomms1336',
        "technical_validation": False,
    },
    {
        "organism": 'Akçaağaç tohumunun dönerek inişi',
        "category": 'Hafif Yapılar ve Aerodinamik',
        "keywords": [
            'küçük sensörü havadan bırakmak',
            'paket düşüşte çok hızlanıyor',
            'pasif iniş düzeneği',
        ],
        "mechanism": 'Dönerek düşen kanatlı tohumun ön kenarındaki girdap kaldırma kuvvetine katkı sağlar.',
        "solution": 'Hafif sensör paketi için tek kanatlı, pasif dönen bir iniş taşıyıcısı.',
        "pilot_test": 'Kapalı düzende aynı kütledeki paketlerin iniş hızını ve yatay sapmasını ölçün.',
        "source_title": 'Leading-edge vortices elevate lift of autorotating plant seeds',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/19520959/',
        "technical_validation": False,
    },
    {
        "organism": 'Lif kabağının gözenekli iskeleti',
        "category": 'Ambalaj ve Darbe Dayanımı',
        "keywords": [
            'kargoda ürün darbe alıyor',
            'ambalaj dolgusu çöküyor',
            'hafif darbe emici dolgu',
        ],
        "mechanism": 'Lif kabağının üç boyutlu lif ağı basınç altında şekil değiştirerek enerji yutar.',
        "solution": 'Aynı kütledeki standart dolguya karşı gözenekli lif ağı biçiminde ambalaj içliği.',
        "pilot_test": 'Standart bir düşürme deneyinde ürünün gördüğü tepe ivmeyi ve dolgunun kalıcı ezilmesini ölçün.',
        "source_title": 'Mechanical properties of luffa sponge',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/23032434/',
        "technical_validation": False,
    },
    {
        "organism": 'Aristolochia sarmaşığının kendini onaran gövdesi',
        "category": 'Malzeme ve Yüzey Tasarımı',
        "keywords": [
            'kaplamada mikro çatlak oluşuyor',
            'ince yüzey çatlağı büyüyor',
            'çatlakları erken kapatmak',
        ],
        "mechanism": 'Gövde dokuları, büyüme gerilmeleriyle açılan lezyonlara aşamalı bir onarım tepkisi verir.',
        "solution": 'Yüzey çizildiğinde boşluğa şişerek dolması amaçlanan alt katmanlı kaplama.',
        "pilot_test": 'Aynı genişlikte çizikler açıp kapanma süresini ve geçirgenlik değişimini ölçün.',
        "source_title": 'Morphological aspects of self-repair of lesions caused by internal growth stresses in stems of Aristolochia macrophylla and Aristolochia ringens',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/20236971/',
        "technical_validation": False,
    },
    {
        "organism": 'Çöl yosununun su toplayan kıl uçları',
        "category": 'Su Hasadı ve Yüzey Tasarımı',
        "keywords": [
            'sisten su toplamak',
            'sis damlaları yüzeye tutunmuyor',
            'nemli havadan damla toplamak',
        ],
        "mechanism": 'Syntrichia caninervis yosununun kıl uçlarındaki farklı ölçeklerde oluklar suyun toplanmasına katkı sağlar.',
        "solution": 'Düz lifler yerine farklı ölçeklerde olukları olan bir sis toplama ağı.',
        "pilot_test": 'Aynı sis akışında birim alan ve saatte toplanan su hacmini karşılaştırın.',
        "source_title": 'How desert moss drinks from air',
        "source_url": 'https://www.nature.com/articles/534155d',
        "technical_validation": False,
    },
    {
        "organism": 'Selaginella’nın kurudukça kıvrılan gövdesi',
        "category": 'Tarım ve Pasif Mekanizmalar',
        "keywords": [
            'kuruyunca yüzey kapansın',
            'kuraklıkta pasif koruma',
            'nem düşünce gölgeleme',
        ],
        "mechanism": 'Selaginella lepidophylla kuruma sırasında gövdelerini içe kıvırır. Araştırma bu davranışın ışık kaynaklı hasarı sınırlamadaki rolünü inceler.',
        "solution": 'Kuruma sırasında hassas yüzeyi örten higromorfik bir kapak.',
        "pilot_test": 'Nem döngüsünde kaplanan alanı ve korunan yüzeye düşen ışığı ölçün.',
        "source_title": 'Reduced photoinhibition with stem curling in the resurrection plant Selaginella lepidophylla',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/28312632/',
        "technical_validation": False,
    },
    {
        "organism": 'Mürekkep balığının değişken ışıkta kamuflajı',
        "category": 'Optik ve Yüzey Tasarımı',
        "keywords": [
            'ışık değişince desen kayboluyor',
            'değişken ışıkta yüzey deseni',
            'arka plan kontrastı değişiyor',
        ],
        "mechanism": 'Mürekkep balığı dinamik aydınlatmada vücut desenini değiştirerek görünür sınırlarını kesintiye uğratabilir.',
        "solution": 'Arka plan ışığına göre kontrast desenini değiştiren düşük çözünürlüklü yüzey paneli.',
        "pilot_test": 'Farklı ışık koşullarında nesne sınırlarının algılanma oranını ölçün.',
        "source_title": 'Cuttlefish adopt disruptive camouflage under dynamic lighting',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/38959882/',
        "technical_validation": False,
    },
    {
        "organism": 'Karahindibanın gözenekli paraşütü',
        "category": 'Hafif Yapılar ve Aerodinamik',
        "keywords": [
            'gözenekli paraşüt tasarımı',
            'sensör havada daha uzun kalsın',
            'düşüşü hafif liflerle yavaşlatmak',
        ],
        "mechanism": 'Karahindibanın geçirgen lif halkası üzerinde ayrık bir girdap oluşur ve bu akış düzeni havada kalmasına katkı sağlar.',
        "solution": 'Hafif işaretleyici için katı disk yerine açık lif halkalı frenleyici.',
        "pilot_test": 'Aynı kütlede geçirgen ve katı modellerin düşüş hızını ve salınımını ölçün.',
        "source_title": 'A separated vortex ring underlies the flight of the dandelion',
        "source_url": 'https://www.nature.com/articles/s41586-018-0604-2',
        "technical_validation": False,
    },
    {
        "organism": 'Sahra gümüş karıncasının üçgen tüyleri',
        "category": 'Isı ve Enerji Yönetimi',
        "keywords": [
            'güneşte kutu aşırı ısınıyor',
            'pasif soğutma yüzeyi',
            'açık alandaki sensör ısınıyor',
        ],
        "mechanism": 'Üçgen kesitli tüyler gelen güneş ışığının yansımasına ve orta kızılötesi ısıl yayımın artmasına katkı sağlar.',
        "solution": 'Yüksek güneş yansıtıcılığı ve ısıl yayım hedefleyen bir dış muhafaza yüzeyi.',
        "pilot_test": 'Aynı güneş altında eş geometrili kutuların iç sıcaklığını ve soğuma hızını kaydedin.',
        "source_title": 'Keeping cool: Enhanced optical reflection and radiative heat dissipation in Saharan silver ants',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/26089358/',
        "technical_validation": False,
    },
    {
        "organism": 'Nepenthes’in ıslandığında kayganlaşan kenarı',
        "category": 'Islak Yüzeyler ve Akış',
        "keywords": [
            'damlalar oluğa yönelmiyor',
            'ıslak yüzeyde kontrollü kayma',
            'sıvıyı tek yöne yönlendirmek',
        ],
        "mechanism": 'Bazı Nepenthes türlerinin tuzak ağzı ıslandığında ince su filmi böceklerin tutunmasını azaltır.',
        "solution": 'Islanınca damlaları belirli bir çıkışa taşıyan mikro oluklu yüzey.',
        "pilot_test": 'Oluklu ve düz yüzeyde damlanın ilerleme yönünü ve yüzeyde kalan sıvıyı ölçün.',
        "source_title": 'Form follows function: morphological diversification and alternative trapping strategies in carnivorous Nepenthes pitcher plants',
        "source_url": 'https://doi.org/10.1111/j.1420-9101.2011.02406.x',
        "technical_validation": False,
    },
    {
        "organism": 'Yabani buğdayın nemle hareket eden kılçıkları',
        "category": 'Tarım ve Pasif Mekanizmalar',
        "keywords": [
            'parça nem değiştikçe ilerlesin',
            'motorsuz küçük hareket',
            'nemle çalışan tek yönlü mekanizma',
        ],
        "mechanism": 'Kılçıklar nem döngüsünde açılıp kapanır. Yönlü yüzey çıkıntıları tohum biriminin hareketini yönlendirir.',
        "solution": 'Nem çevrimlerinden yararlanan tek yönlü küçük parça ilerletici.',
        "pilot_test": 'Kontrollü nem çevriminde çevrim başına hareketi ve geri kayma miktarını ölçün.',
        "source_title": 'The role of wheat awns in the seed dispersal unit',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/17495170/',
        "technical_validation": False,
    },
    {
        "organism": 'Orman kurbağasının donma sırasında glikoz kullanımı',
        "category": 'Soğuk Zincir ve Biyomalzemeler',
        "keywords": [
            'hücreler donarken zarar görüyor',
            'dondurulan hücre canlılığı düşüyor',
            'donma çözülmede hücre kaybı',
        ],
        "mechanism": 'Rana sylvatica dokularında glikoz düzeyi, deneysel olarak donma toleransıyla ilişkilendirilmiştir.',
        "solution": 'Araştırma ölçeğinde koruyucu formülasyon seçimi için ozmotik stres ve donma hasarını birlikte izleme.',
        "pilot_test": 'Yetkili laboratuvarda uygun bir model sistemde farklı formülasyonlarla çözülme sonrası canlılığı karşılaştırın.',
        "source_title": 'Glucose concentration regulates freeze tolerance in the wood frog Rana sylvatica',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/8409827/',
        "technical_validation": False,
    },
    {
        "organism": 'Halkalı örümcek ağının sesi algılaması',
        "category": 'Sensörler ve Otomasyon',
        "keywords": [
            'makineden gelen arıza sesi',
            'geniş alanda zayıf titreşim',
            'arıza sesini erken duymak',
        ],
        "mechanism": 'Halkalı ağ, havadaki sesle titreşerek örümceğin algılayabileceği mekanik sinyal üretir.',
        "solution": 'Gergin lifli bir yüzeyin küçük titreşim algılayıcılarına bağlandığı arıza izleme prototipi.',
        "pilot_test": 'Bilinen arıza sesleri ve arka plan gürültüsünde algılama eşiğini ölçün.',
        "source_title": 'Outsourced hearing in an orb-weaving spider that uses its web as an auditory sensor',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9169088/',
        "technical_validation": False,
    },
    {
        "organism": 'Lithops’un saydam yaprak pencereleri',
        "category": 'Optik ve Görüntüleme',
        "keywords": [
            'rafın alt katına ışık ulaşmıyor',
            'iç bölgeye gün ışığı taşımak',
            'bitki rafında gölgelenme',
        ],
        "mechanism": 'Lithops yaprağındaki epidermal pencereler ışığın yaprak içine girdiği optik bölgeler oluşturur.',
        "solution": 'Yoğun yetiştirme raflarında ışığı karanlık iç bölgelere taşıyan saydam giriş yüzeyleri.',
        "pilot_test": 'Aynı ışık kaynağı altında farklı derinliklerdeki ışık dağılımını karşılaştırın.',
        "source_title": 'The influence of epidermal windows on the light environment within the leaves of six succulents',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/18436541/',
        "technical_validation": False,
    },
    {
        "organism": 'Tabanca karidesinin çöken kabarcığı',
        "category": 'Akış ve Yüzey Temizliği',
        "keywords": [
            'girintideki yüzeyi temassız temizlemek',
            'su jeti darbeleri ölçmek',
            'dar boşluktaki kalıntıyı çıkarmak',
        ],
        "mechanism": 'Hızlı kıskaç hareketi su jeti oluşturur. Jetin oluşturduğu kavitasyon kabarcığı çökerken basınç darbesi meydana gelir.',
        "solution": 'Kapalı test düzeneğinde yerel su jeti darbeleriyle temassız yüzey temizliği deneyi.',
        "pilot_test": 'Numunede kalan tortuyu ve yüzey hasarını farklı jet ayarlarında birlikte ölçün.',
        "source_title": 'How snapping shrimp snap: through cavitating bubbles',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/11000111/',
        "technical_validation": False,
    },
    {
        "organism": 'Kıyı istiridyesi örtüsünün dalgaları sönümlemesi',
        "category": 'Kıyı ve Su Yönetimi',
        "keywords": [
            'küçük dalgalar kıyıyı aşındırıyor',
            'liman içinde dalga azaltmak',
            'yapay resif modülü tasarlamak',
        ],
        "mechanism": 'Laboratuvar çalışması, yapay resif toplarındaki istiridye örtüsü yoğunluğunun dalga sönümlemesiyle ilişkisini inceler.',
        "solution": 'Dalga kanalında gözenekli resif modülleri ve farklı yüzey örtüsü oranlarını karşılaştıran ön tasarım.',
        "pilot_test": 'Aynı giriş dalgasında modül arkasındaki dalga yüksekliğini ve su geçişini ölçün.',
        "source_title": 'Wave attenuation by artificial reef balls with varying oyster coverage density for coastal protection',
        "source_url": 'https://www.sciencedirect.com/science/article/pii/S0029801826014617',
        "technical_validation": True,
    },
    {
        "organism": 'Chiton’un manyetit içeren kazıyıcı dişleri',
        "category": 'Malzeme ve Aşınma Dayanımı',
        "keywords": [
            'kazıyıcı uç çabuk aşınıyor',
            'aşındırıcı yüzeyde uç ömrü',
            'sert uçla esnek gövde',
        ],
        "mechanism": 'Chiton’un radula dişlerinde mineralize manyetit bulunur. Dişin yapısında mineral dağılımı ve kristallerin özellikleri incelenmiştir.',
        "solution": 'Yerel sert parçacıklarla güçlendirilen, değiştirilebilir kazıma ucu.',
        "pilot_test": 'Aynı yükte kazıma çevrimleri boyunca kütle kaybını ve uç geometrisinin değişimini ölçün.',
        "source_title": 'Magnetic and structural properties of magnetite in radular teeth of chiton Acanthochiton rubrolinestus',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/21365666/',
        "technical_validation": False,
    },
]

# Kaynak bağlantılı 148 yeni model ve örnek işletme ifadeleri.
model_catalog.extend([
    {
        "organism": 'Denizkestanesi dikeninin gözenekli iskeleti',
        "category": 'Hafif Yapılar',
        "keywords": [
            'gözenekli çubuk yükte çöküyor',
            'hafif silindirik destek kırılıyor',
            'ince kolonun içini boşaltmak',
        ],
        "mechanism": 'Dikendeki mineral iskelet üç boyutlu gözenekli bir ağ oluşturur.',
        "solution": 'Gözenekleri bölgesel olarak değişen hafif silindirik destek.',
        "pilot_test": 'Eş kütlede basma yükünü ve kırılma biçimini ölçün.',
        "source_title": 'Echinoderm stereom gradient structures enable mechanoelectrical perception',
        "source_url": 'https://doi.org/10.1038/s41586-026-10164-9',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Pomelo kabuğunun katmanlı köpüğü',
        "category": 'Ambalaj ve Darbe',
        "keywords": [
            'ağır meyve düşerken hasarlanıyor',
            'kalın ambalaj geri sekiyor',
            'katmanlı köpük darbe testi',
        ],
        "mechanism": 'Kalın kabuk farklı yapıdaki katmanlarıyla darbe enerjisini yayar.',
        "solution": 'Sert dış deri ve dereceli gözenekli iç dolgudan ambalaj.',
        "pilot_test": 'Düşürme testinde tepe ivme ve kalıcı deformasyonu karşılaştırın.',
        "source_title": 'Pomelo-inspired shear-stiffening/porous bilayer composites with structural tunability for synergistic impact resistance and thermal management',
        "source_url": 'https://www.sciencedirect.com/science/article/abs/pii/S1359836826005822',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Macadamia kabuğunun çatlak yönlendirmesi',
        "category": 'Malzeme Dayanımı',
        "keywords": [
            'kuruyemiş kırıcı muhafazası çatlıyor',
            'sert kabukta çatlak sapması',
            'kabuk paneli ezilmeden çatlıyor',
        ],
        "mechanism": 'Kabuğun farklı yönlenmiş hücreleri çatlağın izlediği yolu etkiler.',
        "solution": 'Yönlenmesi değişen lifli koruyucu kabuk.',
        "pilot_test": 'Çentikli numunede çatlak ilerleme enerjisini ölçün.',
        "source_title": 'Mechanical behavior of macadamia nutshells',
        "source_url": 'https://www.sciencedirect.com/science/article/pii/S2452321620303206',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Hindistan cevizi lifli kabuğunun çekme ağı',
        "category": 'Ambalaj ve Darbe',
        "keywords": [
            'koruyucu kabuk düşüşte dağılıyor',
            'lifli ambalaj bütünlüğünü yitiriyor',
            'düşmede kabuk parçalanmasını azaltmak',
        ],
        "mechanism": 'Dış kabuğun lifleri darbe altında yük taşır ve şekil değiştirir.',
        "solution": 'Darbe sırasında parçaları tutan lifli dış sargı.',
        "pilot_test": 'Düşürme sonrası kopan parça sayısını ve tepe ivmeyi ölçün.',
        "source_title": 'Fruit Biology of Coconut (Cocos nucifera L.)',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9738799/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Deniz salyangozu Strombus kabuğunun çapraz lamelleri',
        "category": 'Malzeme Dayanımı',
        "keywords": [
            'sert kabuk keskin çatlıyor',
            'lamelli seramikte kırılma',
            'gevrek parçada çatlak yayılıyor',
        ],
        "mechanism": 'Çapraz lameller çatlakları saptıran çok düzeyli bir düzen oluşturur.',
        "solution": 'Yönleri dönüşümlü seramik benzeri katman yapısı.',
        "pilot_test": 'Aynı kalınlıkta kırılma işi ve çatlak yolunu karşılaştırın.',
        "source_title": 'Structural basis for the fracture toughness of the shell of the conch Strombus gigas',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/10890440/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Pangolinin üst üste binen pulları',
        "category": 'Koruyucu Tasarım',
        "keywords": [
            'esnek kılıf kesilmeye dayanmıyor',
            'hareketli koruyucu eklem açık kalıyor',
            'zırh plakaları bükülmeyi engelliyor',
        ],
        "mechanism": 'Üst üste binen keratin pullar esnek bir gövde üzerinde örtüşür.',
        "solution": 'Birbirini örten küçük koruyucu plakalardan mafsallı kılıf.',
        "pilot_test": 'Bükülme açıklığı ile delinme direncini birlikte ölçün.',
        "source_title": 'Pangolin armor: Overlapping, structure, and mechanical properties of the keratinous scales',
        "source_url": 'https://www.sciencedirect.com/science/article/pii/S174270611630246X',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Armadillonun hareketli zırh bantları',
        "category": 'Koruyucu Tasarım',
        "keywords": [
            'koruma bandı eğilirken boşluk bırakıyor',
            'eklem kalkanı çok rijit',
            'zırh parçaları hareketle ayrılıyor',
        ],
        "mechanism": 'Sert kemiksi plakalar gövdenin hareketli bantlarında esnek bağlantılarla birleşir.',
        "solution": 'Birbirine bağlı sert modüllerden hareketli koruyucu bant.',
        "pilot_test": 'Belirli bükülme açısında açık alanı ve temas yükünü ölçün.',
        "source_title": 'Armadillo armor: mechanical testing and micro-structural evaluation',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/21565719/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Timsah derisinin kemiksi plakaları',
        "category": 'Koruyucu Tasarım',
        "keywords": [
            'koruyucu yüzey noktasal darbede çöküyor',
            'darbe panelinde sert ada tasarımı',
            'esnek yüzeye sert parçalar koymak',
        ],
        "mechanism": 'Derideki kemiksi plakalar yumuşak dokularla birleşerek bölgesel koruma sağlar.',
        "solution": 'Esnek taşıyıcıya gömülü sert koruma adaları.',
        "pilot_test": 'Eş kütlede noktasal darbe sonrası çökme derinliğini ölçün.',
        "source_title": 'Alligator osteoderms: Mechanical behavior and hierarchical structure',
        "source_url": 'https://www.sciencedirect.com/science/article/pii/S0928493113006371',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Kirpinin içi boş dikenleri',
        "category": 'Ambalaj ve Darbe',
        "keywords": [
            'ince darbe kolonu ani kırılıyor',
            'koruma tamponu kontrollü ezilmiyor',
            'içi boş darbe emici çıkıntı',
        ],
        "mechanism": 'Dikenlerin kabuk ve iç bölmelerden oluşan yapısı bükülme davranışını etkiler.',
        "solution": 'İç bölmeli ince borulardan kontrollü ezilen tampon.',
        "pilot_test": 'Basma eğrisinden yutulan enerjiyi ve tepe kuvvetini hesaplayın.',
        "source_title": 'Dynamic impact testing of hedgehog spines using a dual-arm crash pendulum',
        "source_url": 'https://www.sciencedirect.com/science/article/pii/S175161611630039X',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Afrika oklu kirpisinin diken iç yapısı',
        "category": 'Hafif Yapılar',
        "keywords": [
            'hafif boru ovalleşip çöküyor',
            'boru iç dolgusu fazla ağır',
            'ince tüp eğilmede eziliyor',
        ],
        "mechanism": 'Dikenin hafif iç çekirdeği dış duvarı destekleyen bir kompozit oluşturur.',
        "solution": 'Düşük yoğunluklu çekirdekli ince duvarlı boru.',
        "pilot_test": 'Üç nokta eğmede kütle başına dayanımı karşılaştırın.',
        "source_title": 'Axial compression of a hollow cylinder filled with foam: a study of porcupine quills',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/22982420/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Bal peteğinin altıgen hücreleri',
        "category": 'Hafif Yapılar',
        "keywords": [
            'geniş panelin içi çok ağır',
            'panel çekirdeği basmada çöküyor',
            'sandviç panel hücre geometrisi',
        ],
        "mechanism": 'Arı peteği ortak duvarlı hücrelerden oluşur.',
        "solution": 'Eş kütlede farklı hücre boyutlarına sahip sandviç panel çekirdeği.',
        "pilot_test": 'Basma ve eğilme testinde kütle başına rijitliği ölçün.',
        "source_title": 'The mechanics of honeycombs',
        "source_url": 'https://www.cambridge.org/core/books/abs/cellular-solids/the-mechanics-of-honeycombs/FC24E44367416B6D277BA28D3678E301',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Yusufçuk kanadının oluklu kesiti',
        "category": 'Hafif Yapılar',
        "keywords": [
            'ince levha yük altında sarkıyor',
            'kanat kabuğu rijitliğini artırmak',
            'düz film eğilmede çok esnek',
        ],
        "mechanism": 'Kanat damarları ve oluklu kesit ince kanadın bükülme davranışını belirler.',
        "solution": 'Aynı kütlede oluklu ve düz ince levha karşılaştırması.',
        "pilot_test": 'Üç nokta eğmede yük ve sehim eğrisini çıkarın.',
        "source_title": 'How do dragonfly wings work? A brief guide to functional roles of wing structural components',
        "source_url": 'https://www.tandfonline.com/doi/full/10.1080/13887890.2019.1677515',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Victoria nilüferinin damarlı yaprağı',
        "category": 'Hafif Yapılar',
        "keywords": [
            'geniş tabla ortadan sarkıyor',
            'yüzer tabla yükü dağıtamıyor',
            'ince tablada radyal kaburga',
        ],
        "mechanism": 'Yaprağın altındaki kalın radyal damarlar daha ince bağlantılarla ağ oluşturur.',
        "solution": 'Radyal ve halkasal kaburgalarla güçlendirilmiş geniş tabla.',
        "pilot_test": 'Aynı kütlede farklı yük noktalarındaki sehimi ölçün.',
        "source_title": 'Gigantic floating leaves occupy a large surface area at an economical material cost',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/35138898/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Atkuyruğu gövdesinin silisli yüzeyi',
        "category": 'Malzeme Dayanımı',
        "keywords": [
            'hafif gövdede mineral takviye',
            'ince kabuk sertliğini artırmak',
            'yüzey mineral parçacıkla güçlensin',
        ],
        "mechanism": 'Atkuyruğu dokularında silis belirli yüzey ve hücre bölgelerinde birikir.',
        "solution": 'Yüksek yüzey sertliği için yerel mineral birikimli ince kabuk.',
        "pilot_test": 'Mineral katkılı ve katkısız örneklerde yüzey sertliğini ölçün.',
        "source_title": 'Ultrastructural features of the internodes’ surface in horsetail (Equisetum arvense L.)',
        "source_url": 'https://www.phytomorphology.com/abstract/ultrastructural-features-of-the-internodes-surface-in-horsetail-equisetum-arvense-l-3997.html',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Bambu boğumunun iç diyaframı',
        "category": 'Hafif Yapılar',
        "keywords": [
            'içi boş profil birleşimde eziliyor',
            'boru boyunca destek aralığı',
            'yerel göçmeyi iç halkayla önlemek',
        ],
        "mechanism": 'Bambu boğumunda iç diyafram ve değişen lif yapısı bulunur.',
        "solution": 'Aralıklı iç diyaframları olan boru prototipi.',
        "pilot_test": 'Aynı kütlede yerel ezilme yükünü ve hasar yerini karşılaştırın.',
        "source_title": 'A comprehensive evaluation of the effects of bamboo nodes on the mechanical properties of bamboo culms',
        "source_url": 'https://www.sciencedirect.com/science/article/pii/S0141029623013901',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Ağaçkakan dilinin uzun hiyoid desteği',
        "category": 'Hafif Yapılar',
        "keywords": [
            'dar gövdede uzun esnek bağlantı saklamak',
            'esnek şeridi kavisli yoldan geçirmek',
            'uzun uzantı küçük gövdeye sığmıyor',
        ],
        "mechanism": 'Uzun hiyoid yapı kafatasının etrafını dolaşır ve dilin uzanmasına katkı verir.',
        "solution": 'Esnek aktarma şeridini gövde çevresinden yönlendiren düzenek.',
        "pilot_test": 'Aynı gövde hacminde uzanma mesafesini ve sürtünmeyi ölçün.',
        "source_title": 'Structural analysis of the tongue and hyoid apparatus in a woodpecker',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC5063634/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Tukan gagasının hafif sandviç yapısı',
        "category": 'Hafif Yapılar',
        "keywords": [
            'uzun uzantı ağırlığı artırıyor',
            'hafif dış kabuk rijit kalmalı',
            'ince kabuk ve köpük çekirdek',
        ],
        "mechanism": 'Gaganın keratin dış kabuğu hafif hücresel bir iç yapıyı çevreler.',
        "solution": 'İnce kabuklu ve düşük yoğunluklu çekirdekli uzun muhafaza.',
        "pilot_test": 'Eş kütlede eğilme rijitliği ve hasar başlangıcını ölçün.',
        "source_title": 'The toucan beak: Structure and mechanical response',
        "source_url": 'https://doi.org/10.1016/j.msec.2005.08.025',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Boynuzgaga gagasının lifli kompoziti',
        "category": 'Hafif Yapılar',
        "keywords": [
            'kavisli hafif koruma kapağı',
            'ince kavisli kabuk çatlıyor',
            'gözenekli çekirdekle kavisli panel',
        ],
        "mechanism": 'Boynuzgaga gagasında keratin kabuk ve hafif iç yapı birlikte çalışır.',
        "solution": 'İç geometrisi kademeli kavisli muhafaza.',
        "pilot_test": 'Basma ve eğme testinde tepe yük ve kütleyi karşılaştırın.',
        "source_title": 'Structure and mechanical behavior of bird beaks',
        "source_url": 'https://escholarship.org/uc/item/7064f0k0',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Gergedan böceğinin kavisli boynuzu',
        "category": 'Hafif Yapılar',
        "keywords": [
            'kavisli tutucu yana doğru esniyor',
            'kanca kesiti yük yönüne göre değişsin',
            'uzun kol torsiyonla eğiliyor',
        ],
        "mechanism": 'Boynuz geometrisi ve kesiti türün dövüşte uyguladığı yük türüyle ilişkilidir.',
        "solution": 'Yük yönüne göre kesiti ayarlanmış kavisli tutucu kol.',
        "pilot_test": 'Eş kütlede eğilme ve burulma rijitliğini ölçün.',
        "source_title": 'Variation in cross‐sectional horn shape within and among rhinoceros beetle species',
        "source_url": 'https://wordpress.clarku.edu/mcculloughlab/wp-content/uploads/sites/739/2023/09/McCullough-et-al.-2015-cross-sectional-horn-shape.pdf',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Bighorn koyununun katmanlı boynuzu',
        "category": 'Malzeme Dayanımı',
        "keywords": [
            'darbe emici katman ayrılıyor',
            'kavisli tampon tekrarlı yükte çatlıyor',
            'keratin benzeri darbe plakası',
        ],
        "mechanism": 'Boynuzun yönlü keratin tabakaları ve tübülleri enerji yutma davranışını etkiler.',
        "solution": 'Yönlü tabakalardan kavisli enerji emici panel.',
        "pilot_test": 'Tekrarlı darbe sonrası emilen enerji ve kalıcı şekil değişimini ölçün.',
        "source_title": 'Microstructure and mechanical properties of different keratinous horns',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6030630/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Narval dişinin dışa açık tübülleri',
        "category": 'Sensörler',
        "keywords": [
            'sensör malzeme gözeneklerinden su ölçsün',
            'sert yüzeyde tuzluluk algılama',
            'koruyucu uç içinden sıvı algılama',
        ],
        "mechanism": 'Dişin dışa açılan kanalcıkları çevredeki sıvıyla temasa olanak verir.',
        "solution": 'Gözenekli koruma katmanından geçen sıvıyla çalışan uç sensörü.',
        "pilot_test": 'Kontrollü çözeltide tepki süresini ve ölçüm sapmasını belirleyin.',
        "source_title": 'Sensory ability in the narwhal tooth organ system',
        "source_url": 'https://doi.org/10.1002/ar.22886',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Denizanasının şeffaf mezogleası',
        "category": 'Optik ve Malzeme',
        "keywords": [
            'yumuşak saydam panel bulanıklaşıyor',
            'esnek jel ışığı geçirsin',
            'şeffaf hidrojel mekanik destek',
        ],
        "mechanism": 'Mezoglea su açısından zengin, saydam ve mekanik destek sağlayan bir dokudur.',
        "solution": 'Optik pencere için lifle güçlendirilmiş saydam hidrojel örneği.',
        "pilot_test": 'Işık geçirgenliğini ve çevrimsel sıkıştırma davranışını ölçün.',
        "source_title": 'What are jellyfish made of?',
        "source_url": 'https://oceanservice.noaa.gov/facts/jellyfish.html',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Çekirge kanadı damarlarının çatlak durdurması',
        "category": 'Malzeme Dayanımı',
        "keywords": [
            'ince zar yırtığı hızla büyüyor',
            'membran çentiği boyunca yırtılma',
            'damarlı film yırtık kontrolü',
        ],
        "mechanism": 'Çekirgenin arka kanadındaki damarlar, ince zar boyunca ilerleyen çatlakların önünde engel oluşturabilir.',
        "solution": 'Zar içinde çatlak yolunu kesen ince takviye hatları.',
        "pilot_test": 'Standart çentikte yırtık uzunluğu ve kopma enerjisini ölçün.',
        "source_title": 'Veins Improve Fracture Toughness of Insect Wings',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC3425546/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Yengeç kıskaç kabuğunun dereceli sertliği',
        "category": 'Malzeme Dayanımı',
        "keywords": [
            'tutucu yüzeyi sert içi tok olsun',
            'sert uç bağlantıdan kopuyor',
            'kıskaç yüzeyi aşınıyor',
        ],
        "mechanism": 'Kıskaç kutikulasında mineral ve yapı dağılımı sertliğin konuma göre değişmesine katkı verir.',
        "solution": 'Sert temas yüzeyinden daha tok gövdeye kademeli geçiş.',
        "pilot_test": 'Sertlik profili ve bağlantı çevresindeki çatlak sayısını ölçün.',
        "source_title": 'Tissue structure and mechanical properties of the exoskeleton of the huge claws of the mud crab, Scylla serrata',
        "source_url": 'https://link.springer.com/article/10.1007/s10853-022-08083-x',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Istakoz kabuğunun helisel lifleri',
        "category": 'Malzeme Dayanımı',
        "keywords": [
            'kompozit panel delaminasyon yapıyor',
            'tabaka açısını değiştirip çatlağı yönlendirmek',
            'lifli kalkan katman kaybı',
        ],
        "mechanism": 'Kutikula, açıları tabakalar arasında dönen lif düzeni içerir.',
        "solution": 'Darbe plakası için kademeli döndürülmüş tabakalar.',
        "pilot_test": 'Darbe sonrası tabakalar arası ayrılma alanını ölçün.',
        "source_title": 'Mechanical and structural gradients in the exoskeleton of the lobster Homarus americanus',
        "source_url": 'https://doi.org/10.1016/j.actamat.2005.05.027',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Kuş yumurtası kabuğunun eğriliği',
        "category": 'Hafif Yapılar',
        "keywords": [
            'ince kubbe basınç altında kırılıyor',
            'oval kabuk yük dağılımı',
            'ince oval muhafaza tasarlamak',
        ],
        "mechanism": 'Eğri mineral kabuğun yük taşıması geometriye ve yük yönüne bağlıdır.',
        "solution": 'Farklı eğriliklere sahip ince koruma kabuğu.',
        "pilot_test": 'Aynı kütlede farklı yönlerden basma yükünü karşılaştırın.',
        "source_title": "Nature's technical ceramic: the avian eggshell",
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/28123095/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Mürekkep balığı kemiğinin odacıkları',
        "category": 'Hafif Yapılar',
        "keywords": [
            'hafif çekirdek aniden parçalanıyor',
            'basma altında ardışık çökme',
            'odacıklı çekirdek tasarımı',
        ],
        "mechanism": 'Sepia iç kabuğundaki odalar ve duvarlar düşük yoğunlukta yük taşır.',
        "solution": 'Kademeli çöken odacıklı panel çekirdeği.',
        "pilot_test": 'Basma deneyinde çökme sırasını ve emilen enerjiyi ölçün.',
        "source_title": 'Mechanical design of the highly porous cuttlebone: A bioceramic hard buoyancy tank for cuttlefish',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/32913055/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Nautilus kabuğunun bölmeli spiral yapısı',
        "category": 'Akışkanlık ve Yüzdürme',
        "keywords": [
            'yüzer cihazın hacmi bölmelere ayrılsın',
            'yüzer platform tek bölme delinince batıyor',
            'bölmeli hacimde kaldırma kontrolü',
        ],
        "mechanism": 'Bölmeli kabuk ve sifunkul, odacıkların sıvı içeriğini düzenleyerek yüzdürmeye katkı sağlar.',
        "solution": 'Bağımsız odacıklı yüzdürme prototipi.',
        "pilot_test": 'Tek odacık su aldığında kalan yüzdürme kuvvetini ölçün.',
        "source_title": 'What is a nautilus?',
        "source_url": 'https://oceanservice.noaa.gov/facts/nautilus.html?dom=prime&src=syn',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Gümüş kanatlı Argyrophorus kelebeğinin optik pulları',
        "category": 'Optik Yüzeyler',
        "keywords": [
            'metalik boya olmadan parlak yüzey',
            'geniş bant parlak kaplama',
            'parlak etiket pigmentsiz olsun',
        ],
        "mechanism": 'Argyrophorus argenteus kanat pullarının optik yapısı geniş dalga boyu aralığında gümüşümsü yansıma üretir.',
        "solution": 'Metal pigment kullanmadan ince katmanlı yansıtıcı işaret.',
        "pilot_test": 'Dalga boyu ve açıya göre yansıma dağılımını ölçün.',
        "source_title": 'Optical costs and benefits of disorder in biological photonic crystals',
        "source_url": 'https://pubs.rsc.org/en/content/articlehtml/2020/fd/d0fd00101e',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Güve gözünün yansıma azaltan çıkıntıları',
        "category": 'Optik Yüzeyler',
        "keywords": [
            'ekran camı güneşte yansıyor',
            'optik pencere parlıyor',
            'yansıma azaltan nano doku',
        ],
        "mechanism": 'Dalga boyundan küçük düzenli çıkıntılar kırılma indisi geçişini kademelendirir.',
        "solution": 'Optik kapak üzerinde küçük çıkıntılı yansıma azaltıcı doku.',
        "pilot_test": 'Görünür aralıkta açıya bağlı yansımayı karşılaştırın.',
        "source_title": 'Optical Modelling and Phylogenetic Analysis Provide Clues to the Likely Function of Corneal Nipple Arrays in Butterflies and Moths',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6780202/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Cicada kanadının nanodokusu',
        "category": 'Yüzey Hijyeni',
        "keywords": [
            'yüzeyde bakteri tutunuyor',
            'kimyasal içermeyen bakteri yüzeyi',
            'temas yüzeyi mikro doku denemesi',
        ],
        "mechanism": 'Bazı ağustosböceği kanatlarındaki nano çıkıntılar belirli bakterilerin hücre zarfını etkiler.',
        "solution": 'Laboratuvar değerlendirmesi için nano dokulu numune.',
        "pilot_test": 'Yetkili laboratuvarda aynı bakteri türünde canlı yüzey yükünü ölçün.',
        "source_title": 'Natural Bactericidal Surfaces: Mechanical Rupture of Pseudomonas aeruginosa Cells by Cicada Wings',
        "source_url": 'https://onlinelibrary.wiley.com/doi/full/10.1002/smll.201200528',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Zıplayan örümcek pullarının gökkuşağı deseni',
        "category": 'Optik Yüzeyler',
        "keywords": [
            'açıyla değişen güvenlik etiketi',
            'renkli holografik kontrol işareti',
            'çok küçük renk kodu üretmek',
        ],
        "mechanism": 'Maratus örümceklerinin bazı pullarında kırınım oluşturan nanogeometri bulunur.',
        "solution": 'Farklı bakış açılarında belirgin desen veren optik etiket.',
        "pilot_test": 'Açıya bağlı renk ayrımını ve okuma hata oranını ölçün.',
        "source_title": 'Rainbow peacock spiders inspire miniature super-iridescent optics',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/29273708/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Bukalemunun ayarlanabilir kristal aralığı',
        "category": 'Optik Yüzeyler',
        "keywords": [
            'gerilince renk değiştiren şerit',
            'mekanik durum renk ile görünsün',
            'renk göstergesi boya kullanmasın',
        ],
        "mechanism": 'İridoforlardaki guanin kristallerinin aralık değişimi yansıyan rengi kaydırır.',
        "solution": 'Deformasyona tepki veren yapısal renkli durum göstergesi.',
        "pilot_test": 'Bilinen gerinimlerde renk kaymasını ve histerezisi ölçün.',
        "source_title": 'Photonic crystals cause active colour change in chameleons',
        "source_url": 'https://www.nature.com/articles/ncomms7368',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Altın kaplumbağa böceğinin nem kontrollü rengi',
        "category": 'Optik Yüzeyler',
        "keywords": [
            'paketin içine nem girince renk değişsin',
            'nem değişimi optik uyarı',
            'suya bağlı yapısal renk',
        ],
        "mechanism": 'Böceğin katmanlı optik yapısındaki sıvı durumu yansımayı değiştirir.',
        "solution": 'Nemle değişen renkli pasif gösterge katmanı.',
        "pilot_test": 'Nem döngüsünde renk farkı ve geri dönüş süresini ölçün.',
        "source_title": 'Switchable reflector in the Panamanian Tortoise Beetle Charidotella egregia (Chrysomelidae: Cassidinae)',
        "source_url": 'https://repository.si.edu/items/f348b3e2-faac-4ec3-8e88-1b9962e3e0e1',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Pollia meyvesinin selüloz kaynaklı rengi',
        "category": 'Optik Yüzeyler',
        "keywords": [
            'pigmentsiz mavi ürün etiketi',
            'renk kimyasalsız elde edilsin',
            'selülozla parlak yüzey',
        ],
        "mechanism": 'Selüloz liflerinin helisel düzeni seçili dalga boylarını yansıtır.',
        "solution": 'Selüloz bazlı yapısal renkli işaret veya kaplama.',
        "pilot_test": 'Açıya bağlı spektrumu ve yaşlandırma sonrası renk değişimini ölçün.',
        "source_title": 'Pointillist structural color in Pollia fruit',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/23019355/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Begonya yaprağının fotonik kloroplastları',
        "category": 'Optik Yüzeyler',
        "keywords": [
            'zayıf ışıkta optik katman tasarlamak',
            'fotonik yansımayı biyolojik katmanla ayarlamak',
            'ince katmanda seçici ışık kullanımı',
        ],
        "mechanism": 'Bazı Begonia türlerinde düzenli iç membran katmanları optik özelliklere katkı verir.',
        "solution": 'Düşük ışık koşulunda belirli dalga boyunu yöneten katman prototipi.',
        "pilot_test": 'Katmanlı ve kontrol örneğinde spektral geçirgenliği ölçün.',
        "source_title": 'Photonic multilayer structure of Begonia chloroplasts enhances photosynthetic efficiency',
        "source_url": 'https://www.nature.com/articles/nplants2016162',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Diatom kabuğunun gözenekli silika düzeni',
        "category": 'Optik ve Filtrasyon',
        "keywords": [
            'saydam mikro gözenekli panel',
            'ışık ve parçacık seçen ince tabaka',
            'silika gözenek boyutu tasarımı',
        ],
        "mechanism": 'Diatomların silika kabuğunda düzenli gözenekler bulunur.',
        "solution": 'Işık geçiren mikro gözenekli ayırıcı numunesi.',
        "pilot_test": 'Geçirgenlik spektrumunu ve farklı boyutlardaki parçacık geçişini ölçün.',
        "source_title": 'Diatoms in Focus: Chemically Doped Biosilica for Customized Nanomaterials',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC11639631/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Ağaç kurbağasının kanallı ayak pedleri',
        "category": 'Kavrama ve Robotik',
        "keywords": [
            'ıslak camı tutucu kayıyor',
            'ıslak yüzeyde yumuşak kavrama',
            'cam kavramada su filmi',
        ],
        "mechanism": 'Pedin mikrokanalları sıvı ve temas alanının düzenlenmesine katkı verir.',
        "solution": 'Mikrokanallı yumuşak tutucu pedi.',
        "pilot_test": 'Islak camda kayma başlangıcı kuvvetini ölçün.',
        "source_title": 'Wet but not slippery: Boundary friction in tree frog adhesive toe pads',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/16971337/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Vatozun dalgalanan göğüs yüzgeci',
        "category": 'Su Altı Robotik',
        "keywords": [
            'sualtı robotu pervanesiz ilerlesin',
            'geniş yüzgeçle sessiz manevra',
            'robot yüzgeç dalga hareketi',
        ],
        "mechanism": 'Bazı vatozlarda göğüs yüzgeci boyunca ilerleyen dalgalar itki üretir.',
        "solution": 'Esnek kenarlı dalgalanan yüzgeç düzeneği.',
        "pilot_test": 'Eş giriş gücünde itkiyi ve dönüş yarıçapını ölçün.',
        "source_title": 'Function of the tail in myliobatid rays: role in controlling body stability',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12585887/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Remora balığının tutunma diski',
        "category": 'Kavrama ve Robotik',
        "keywords": [
            'hareketli ıslak yüzeye vantuz tutmuyor',
            'ıslak pürüzlü yüzeye geçici bağlantı',
            'akışta tutunan disk',
        ],
        "mechanism": 'Diskteki dönebilen lameller basınç ve sürtünmeyle tutunmaya katkı verir.',
        "solution": 'Lamelli ve çıkarılabilir ıslak yüzey bağlantısı.',
        "pilot_test": 'Farklı pürüzlülükte kayma ve ayırma yükünü ölçün.',
        "source_title": 'Mechanical underwater adhesive devices for soft substrates',
        "source_url": 'https://www.nature.com/articles/s41586-025-09304-4',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Deniz yıldızının tüp ayak yapışkanı',
        "category": 'Kavrama ve Robotik',
        "keywords": [
            'sualtında kalıcı yapıştırıcı kullanmadan tutunmak',
            'ıslak zemine geçici yapışma',
            'geçici yapışkan su içinde çözülsün',
        ],
        "mechanism": 'Tüp ayaklar geçici bağlanma ve ayrılmayı salgılarla yönetir.',
        "solution": 'Ayrı bağlama ve salma aşamaları olan ıslak tutucu.',
        "pilot_test": 'Tekrarlı çevrimlerde tutunma kuvvetini ve kalıntıyı ölçün.',
        "source_title": 'Characterisation of the carbohydrate fraction of the temporary adhesive secreted by the tube feet of the sea star Asterias rubens',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/20886254/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Deniz atının kare kesitli kuyruğu',
        "category": 'Kavrama ve Robotik',
        "keywords": [
            'robot kuyruğu ezilince kavrayamıyor',
            'kare segmentli robot tutucu',
            'esnek kol basmada şekli korusun',
        ],
        "mechanism": 'Kare kesitli kemik plakalar kavrama ve sıkışma sırasında hareket edebilir.',
        "solution": 'Kare halkalı ve mafsallı esnek tutucu.',
        "pilot_test": 'Kavrama torkunu ve sıkıştırma sonrası toparlanmayı ölçün.',
        "source_title": 'Seahorses benefit from square tails',
        "source_url": 'https://www.nature.com/articles/523131e',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Yılan pullarının yönlü sürtünmesi',
        "category": 'Kavrama ve Robotik',
        "keywords": [
            'sürünerek ilerleyen robot geri kayıyor',
            'yönlü sürtünme ile taşıma',
            'zeminde tek yönlü tutuş',
        ],
        "mechanism": 'Karın pulları zeminde yönlere göre farklı sürtünme oluşturabilir.',
        "solution": 'İleri kayıp geri tutan taban dokusu.',
        "pilot_test": 'Her iki yönde sürtünme katsayısını ve ilerleme verimini ölçün.',
        "source_title": 'The mechanics of slithering locomotion',
        "source_url": 'https://hu.gatech.edu/Publications/Hu09.pdf',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Ağaçta yaşayan yılanların kavrayan gövdesi',
        "category": 'Kavrama ve Robotik',
        "keywords": [
            'ince direğe sarılan robot aşağı kayıyor',
            'silindire çevresel kavrama',
            'robot kol direği sıkı tutsun',
        ],
        "mechanism": 'Dala sarılan yılan, gövde boyunca çevresel sıkma kuvveti uygular.',
        "solution": 'Birden fazla segmenti olan sarılabilir dikey tutucu.',
        "pilot_test": 'Farklı çaplarda kayma eşiğini ve enerji tüketimini ölçün.',
        "source_title": 'Arboreal snake locomotion 3871',
        "source_url": 'https://blogs.uakron.edu/astleylab/wp-content/uploads/sites/1471/2018/10/Astley-Jayne-2007-arboreal-concertina-locomotion.pdf',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Dağ keçisinin iki parçalı toynağı',
        "category": 'Kavrama ve Robotik',
        "keywords": [
            'engebeli kayada robot ayağı kayıyor',
            'bölünebilen robot tabanı',
            'kayaya uyumlu tırmanma pedi',
        ],
        "mechanism": 'Çift tırnak ve temas pedleri ayağın farklı yüzeylere uyumuna katkı verir.',
        "solution": 'Bağımsız esneyen çift parçalı robot ayağı.',
        "pilot_test": 'Kontrollü eğimlerde kayma açısını ve temas alanını ölçün.',
        "source_title": 'biomimetics',
        "source_url": 'https://mdpi-res.com/d_attachment/biomimetics/biomimetics-08-00008/article_deploy/biomimetics-08-00008.pdf',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Deve ayağının yükü yayan pedi',
        "category": 'Kavrama ve Robotik',
        "keywords": [
            'tekerlek kuma batıyor',
            'yumuşak zeminde taban basıncı',
            'robot ayağı yük altında genişlesin',
        ],
        "mechanism": 'Geniş yastıklı ayak yükü daha büyük temas alanına yayar.',
        "solution": 'Yük altında genişleyebilen yumuşak taban.',
        "pilot_test": 'Kum yatağında batma derinliğini ve zemin basıncını ölçün.',
        "source_title": 'Biomechanical insights into the role of foot pads during locomotion in camelid species',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC7051995/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Fil hortumunun kas hidrostatı',
        "category": 'Kavrama ve Robotik',
        "keywords": [
            'kırılgan ürünü sararak almak',
            'eklemsiz robot kolu uzatmak',
            'yumuşak kol aynı anda eğilip uzasın',
        ],
        "mechanism": 'Karşılıklı kas düzeni sabit hacme yakın dokuda uzama ve eğilmeyi mümkün kılar.',
        "solution": 'Uzayıp çevresine sarılabilen aktüatör prototipi.',
        "pilot_test": 'Kavrama kuvveti ile uzanma mesafesini karşılaştırın.',
        "source_title": 'Maximum trunk tip force assessment related to trunk position and prehensile ’fingers’ implication in African savannah elephants',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC11093316/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Koalanın karşılıklı tutuşlu pençesi',
        "category": 'Kavrama ve Robotik',
        "keywords": [
            'kalın dalı iki yandan kavramak',
            'düzensiz silindirde karşılıklı parmak',
            'kavrama parmakları farklı açılarda kapansın',
        ],
        "mechanism": 'Ön ayaktaki karşılıklı parmak grupları dalı iki yönden çevreler.',
        "solution": 'Farklı açılarda kapanan iki parmak grubu.',
        "pilot_test": 'Üç silindir çapında taşıma sırasında kaymayı ölçün.',
        "source_title": 'Koala forepaw anatomy',
        "source_url": 'https://museum-publications.australian.museum/media/dd/Uploads/Documents/38145/ANH_vXX_04%2Blowres.57202ab.pdf',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Ağaçkakanın kavrayan çift yönlü parmakları',
        "category": 'Kavrama ve Robotik',
        "keywords": [
            'dikey direğe sabitlenen ayak',
            'iki yönden pençe kavraması',
            'robot ayağı dik yüzeyde tutunsun',
        ],
        "mechanism": 'Parmakların karşılıklı düzeni dik gövdeye tutunmaya katkı sağlar.',
        "solution": 'Karşılıklı kancalı dik yüzey tutucusu.',
        "pilot_test": 'Farklı direk çaplarında maksimum kayma yükünü ölçün.',
        "source_title": 'Woodpeckers: Zygodactyl foot',
        "source_url": 'https://fwra.org/wp-content/uploads/2023/11/Woodpeckers-Natures-Woodworkers.pdf',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Yalıçapkınının sivrilen gagası',
        "category": 'Akış ve Gürültü',
        "keywords": [
            'tren tünele girince basınç dalgası',
            'hızlı tren tünelde gürültü',
            'burun geometrisiyle giriş dalgası',
        ],
        "mechanism": 'Dar ve sivrilen gaga, dalış sırasında suya giriş geometrisini belirler.',
        "solution": 'Tünel giriş basıncını azaltmak için farklı sivrilikte taşıt burunları.',
        "pilot_test": 'Aynı hız ve kesitte basınç gradyanını karşılaştırın.',
        "source_title": 'The Beak That Inspired a Bullet Train — Biological Strategy — AskNature',
        "source_url": 'https://asknature.org/strategy/beak-provides-streamlining/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Yelkenbalığının açılır sırt yüzgeci',
        "category": 'Su Altı Robotik',
        "keywords": [
            'seyirde robot yüzgeci gövdeye kapansın',
            'sualtı aracı manevrada yüzgeç açsın',
            'gerektiğinde büyüyen dümen',
        ],
        "mechanism": 'Büyük sırt yüzgeci açılıp kapanabilir.',
        "solution": 'Seyir ve manevra için açılabilir yardımcı yüzgeç.',
        "pilot_test": 'Açık ve kapalı durumda dönüş yarıçapı ile sürüklemeyi ölçün.',
        "source_title": 'How sailfish use their bills to capture schooling prey',
        "source_url": 'https://doi.org/10.1098/rspb.2014.0444',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Orkinosun ince kuyruk sapı ve orak yüzgeci',
        "category": 'Su Altı Robotik',
        "keywords": [
            'sualtı robotu sabit hızda çok enerji harcıyor',
            'orak kuyrukla uzun seyir',
            'kuyruk sapı sürükleme deneyi',
        ],
        "mechanism": 'İnce kuyruk sapı salınımlı orak yüzgece bağlanır.',
        "solution": 'Uzun süreli seyir için salınımlı orak kuyruk prototipi.',
        "pilot_test": 'Belirli hızda birim mesafe başına enerjiyi ölçün.',
        "source_title": 'The tuna keel is a mechanosensory structure',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC11771206/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Mavi yüzgeçli orkinosun hidrolik yüzgeç kontrolü',
        "category": 'Su Altı Robotik',
        "keywords": [
            'sualtı aracında hidrolik yüzgeç ayarı',
            'hız değişince yüzgeç açısı ayarlansın',
            'düşük basınçla sualtı kanadı hareketi',
        ],
        "mechanism": 'Yüzgeç çevresindeki sıvı basıncı yüzgecin biçimi ve konumunu değiştirebilir.',
        "solution": 'Yumuşak hidrolik bölmeli değişken yüzgeç.',
        "pilot_test": 'Basınca göre yüzgeç açısı ve manevra süresini ölçün.',
        "source_title": 'Hydraulic control of tuna fins: A role for the lymphatic system in vertebrate locomotion',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC5833934/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Uçan balığın geniş göğüs yüzgeçleri',
        "category": 'Hafif Yapılar ve Aerodinamik',
        "keywords": [
            'su üstünden sıçrayan sensör süzülsün',
            'su çıkışında açılan kanat',
            'suya yakın süzülme düzeneği',
        ],
        "mechanism": 'Geniş göğüs yüzgeçleri havada süzülmeye olanak verir.',
        "solution": 'Sudan çıkış sonrası açılan hafif kanat.',
        "pilot_test": 'Kapalı testte süzülme mesafesini ve iniş sapmasını ölçün.',
        "source_title": 'Impact of the pectoral fin geometry on the gliding performance of flying fish robot',
        "source_url": 'https://www.sciencedirect.com/science/article/pii/S266737972600046X',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Bayağı mürekkep balığının yan yüzgeç dalgası',
        "category": 'Su Altı Robotik',
        "keywords": [
            'sualtı kamerası yerinde sabit duramıyor',
            'düşük hızda hassas sualtı hareketi',
            'yan yüzgeçle konum koruma',
        ],
        "mechanism": 'Gövde kenarındaki yüzgeçlerin dalgalanması yavaş yüzüşte gövde duruşunun korunmasına katkı verebilir.',
        "solution": 'Karşılıklı dalgalı yan yüzgeçlerle konum düzeltme.',
        "pilot_test": 'Sabit akıntıda konum hatası ve güç tüketimini ölçün.',
        "source_title": 'The Swimming of Cuttlefish',
        "source_url": 'https://www.nature.com/articles/125893a0',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'İğne balığının yüzeyde sıçraması',
        "category": 'Akış ve Hareket',
        "keywords": [
            'su yüzeyinden aralıklı sıçrama',
            'su hava geçişi robot engeli',
            'robot gövdesi yüzeyden hızla çıkacak',
        ],
        "mechanism": 'İğne balıkları, yüzeyden çıkıp havaya sıçrayabilir.',
        "solution": 'Kısa süreli yüzey geçişi için dar ve hafif gövde prototipi.',
        "pilot_test": 'Yüzeyden çıkış açısını ve sıçrama mesafesini ölçün.',
        "source_title": 'FAO species identification sheets: Belonidae',
        "source_url": 'https://www.fao.org/4/ad468e/ad468eBD.pdf',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Su yürüyen böceğin hidrofobik ayakları',
        "category": 'Su Üstü Robotik',
        "keywords": [
            'minik sensör suya batıyor',
            'su yüzeyinde hafif cihaz hareketi',
            'yüzey gerilimiyle taşıma',
        ],
        "mechanism": 'Su itici mikro tüyler ayakların su yüzeyini delmeden kuvvet iletmesine katkı verir.',
        "solution": 'Hafif cihaz için hidrofobik ince ayaklar.',
        "pilot_test": 'Azami taşınan yükü ve yüzeyin bozulduğu kuvveti ölçün.',
        "source_title": 'Water-repellent legs of water striders',
        "source_url": 'https://www.nature.com/articles/432036a',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Basilisk kertenkelesinin suya vuran ayakları',
        "category": 'Su Üstü Robotik',
        "keywords": [
            'robot su üstünde adımlasın',
            'su yüzeyinde darbeli destek',
            'hareketli ayakla batmayı azaltmak',
        ],
        "mechanism": 'Hızlı ayak vuruşları suya momentum aktararak kısa süreli destek üretir.',
        "solution": 'Hafif deney düzeneğinde darbeli ayak mekanizması.',
        "pilot_test": 'Adım frekansına göre taşınan yükü ve batmayı ölçün.',
        "source_title": 'A hydrodynamic model of locomotion in the Basilisk Lizard',
        "source_url": 'https://www.nature.com/articles/380340a0',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Su dalgıcı örümceğin hava çanı',
        "category": 'Su Altı Robotik',
        "keywords": [
            'sualtı cihazının etrafında hava kabarcığı tutmak',
            'su içinde küçük hava odası',
            'hava çanı oksijen aktarımı',
        ],
        "mechanism": 'Örümcek, ipek yapıda hava tutar ve çanın gaz alışverişinden yararlanır.',
        "solution": 'Gözenekli kafeste kararlı hava cebi deney düzeneği.',
        "pilot_test": 'Derinliğe göre hava hacmi ve gaz değişim hızını ölçün.',
        "source_title": 'The diving bell and the spider: the physical gill of Argyroneta aquatica',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/21653811/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Yunusun akışla etkileşen uzun gövdesi',
        "category": 'Akış ve Hareket',
        "keywords": [
            'su sensörünün burnu akışta sallanıyor',
            'uzun sualtı gövdesi için sivri burun',
            'burun akış ayrılması deneyi',
        ],
        "mechanism": 'Yunus gövdesi boyunca hareket sırasında basınç dağılımı ve akış koşulları değişir.',
        "solution": 'Su sensörü için farklı sivrilikte ön uçlar.',
        "pilot_test": 'Aynı akış hızında sürükleme ve titreşimi ölçün.',
        "source_title": 'Swimming of dolphins: experiments and modelling',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/8571225/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Penguen yüzgecinin bükülen kanat profili',
        "category": 'Su Altı Robotik',
        "keywords": [
            'esnek kanatla su altında itki',
            'robot yüzgeci derinlikte de çalışsın',
            'sualtında çırpan kanat',
        ],
        "mechanism": 'Penguenin ön uzvu su altında çırpılırken bükülebilir. Bu bükülme itki oluşumunu etkiler.',
        "solution": 'Yüzgeç açısı ve esnekliği değiştirilebilen bir su altı kanadı.',
        "pilot_test": 'Çırpma frekansına göre itki ve enerji harcamasını ölçün.',
        "source_title": 'Kinematics and hydrodynamics analyses of swimming penguins: wing bending improves propulsion performance',
        "source_url": 'https://doi.org/10.1242/jeb.242140',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Albatrosun dinamik süzülüşü',
        "category": 'Hafif Yapılar ve Aerodinamik',
        "keywords": [
            'rüzgâr tabakasından enerjiyle süzülmek',
            'insansız planör rüzgârla irtifa kazansın',
            'değişken rüzgârda uçuş rotası',
        ],
        "mechanism": 'Albatros farklı rüzgâr hızlarındaki hava katmanları arasında manevra yaparak enerji kazanır.',
        "solution": 'Rüzgâr gradyanını kullanan planör rota simülasyonu.',
        "pilot_test": 'Aynı meteorolojik profilde irtifa ve enerji değişimini karşılaştırın.',
        "source_title": 'Minimum shear wind strength required for dynamic soaring of albatrosses',
        "source_url": 'https://onlinelibrary.wiley.com/doi/10.1111/j.1474-919x.2004.00295.x',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Harris şahinindeki ayrık kanat uçları',
        "category": 'Hafif Yapılar ve Aerodinamik',
        "keywords": [
            'kanat ucunda girdap kaybı',
            'ayrık kanat uçlarını karşılaştırmak',
            'düşük hızda kanat sürüklemesi',
        ],
        "mechanism": 'Yelpaze gibi açılan uç tüyleri birden fazla ayrık uç oluşturur.',
        "solution": 'Çok parçalı uç profili olan düşük hızlı model kanat.',
        "pilot_test": 'Aynı kaldırmada sürüklemeyi ve uç akışını ölçün.',
        "source_title": "Drag reduction by wing tip slots in a gliding Harris' hawk, Parabuteo unicinctus",
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/9318544/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Sineğin denge organları',
        "category": 'Sensörler',
        "keywords": [
            'mini dron dönüşü geç algılıyor',
            'salınan kütleyle açısal hız',
            'mekanik jiroskop küçük olsun',
        ],
        "mechanism": 'Halterler salınım sırasında dönmenin oluşturduğu Coriolis kuvvetlerini algılar.',
        "solution": 'Salınan küçük kütleli dönüş algılama düzeneği.',
        "pilot_test": 'Bilinen açısal hızlarda gecikmeyi ve ölçüm hatasını ölçün.',
        "source_title": 'Visual input to the efferent control system of a fly\'s "gyroscope"',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/9535659/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Bal arısının optik akışla inişi',
        "category": 'Sensörler',
        "keywords": [
            'dron yere yaklaşırken sert iniyor',
            'kamera akışıyla yumuşak iniş',
            'mesafe sensörsüz iniş kontrolü',
        ],
        "mechanism": 'Arılar inişte görsel sahnenin hareketinden yararlanır.',
        "solution": 'Kamera optik akışına dayalı iniş denetleyicisi.',
        "pilot_test": 'Farklı yüzey dokularında iniş hızını ve temas şiddetini ölçün.',
        "source_title": 'Landing strategies in honeybees, and possible applications to autonomous airborne vehicles',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/11341587/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Yarasanın yankıyla yön bulması',
        "category": 'Sensörler',
        "keywords": [
            'karanlıkta sesle engel algılama',
            'ultrasonla dar alan haritası',
            'dumanlı ortamda yankıdan mesafe',
        ],
        "mechanism": 'Yarasalar yaydıkları çağrıların gecikmesi ve özellikleriyle çevreyi algılar.',
        "solution": 'Çok frekanslı yankı sensörü ile engel algılama prototipi.',
        "pilot_test": 'Kontrollü ortamda mesafe hatası ve ayırt edilen hedef sayısını ölçün.',
        "source_title": 'Bat guilds, a concept to classify the highly diverse foraging and echolocation behaviors of microchiropteran bats',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC3699716/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Fok bıyığının iz algılaması',
        "category": 'Sensörler',
        "keywords": [
            'sualtı akıntısında iz kayboluyor',
            'akıntı türbülansını ince bıyıkla algılamak',
            'robot kendi titreşiminden sinyali ayırsın',
        ],
        "mechanism": 'Dalgalı kesitli bıyık, akış izlerini algılamaya yardımcı olur ve kendi titreşimini sınırlar.',
        "solution": 'Dalgalı kesitli esnek sualtı akış sensörü.',
        "pilot_test": 'Aynı akıntıda iz sinyalini arka plan titreşiminden ayırma oranını ölçün.',
        "source_title": 'Experimental Study on the Effect of the Angle of Attack on the Flow-Induced Vibration of a Harbor Seal’s Whisker',
        "source_url": 'https://www.mdpi.com/2311-5521/8/7/206',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Kedi bıyığının temasla mesafe algısı',
        "category": 'Sensörler',
        "keywords": [
            'robot dar aralıkta çarpıyor',
            'esnek temas sensörüyle boşluk ölçmek',
            'karanlıkta duvara yaklaşma algısı',
        ],
        "mechanism": 'Bıyık büküldüğünde kökteki mekanik algılayıcılar uyarılır.',
        "solution": 'Esnek bıyık dizili temas ve boşluk sensörü.',
        "pilot_test": 'Farklı yaklaşma açılarında temas konumu hatasını ölçün.',
        "source_title": 'On the intrinsic curvature of animal whiskers',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9821693/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Pit engereğinin kızılötesi çukuru',
        "category": 'Sensörler',
        "keywords": [
            'karanlıkta ılık parça algılama',
            'küçük sıcaklık farkını yönlü algılamak',
            'termal sensör görüş açısı deneyi',
        ],
        "mechanism": 'Çukur organındaki zar, ısıl ışınımı algılayan sinir uçlarıyla bağlantılıdır.',
        "solution": 'Yön seçici açıklıklı termal algılama prototipi.',
        "pilot_test": 'Bilinen sıcaklıktaki hedeflerde algılama açısı ve eşiği ölçün.',
        "source_title": 'Molecular Basis of Infrared Detection by Snakes',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC2855400/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Elektrikli balığın aktif elektriksel algısı',
        "category": 'Sensörler',
        "keywords": [
            'bulanık suda elektrik alanla nesne bulmak',
            'görüşsüz suda yakın nesne',
            'iletkenlik farkı ile sualtı algısı',
        ],
        "mechanism": 'Zayıf elektrikli balıklar kendi oluşturdukları alanın nesnelerle bozulmasını algılar.',
        "solution": 'Düşük gerilimli sualtı nesne algılama düzeneği.',
        "pilot_test": 'Nesne uzaklığına ve iletkenliğe göre algılama hatasını ölçün.',
        "source_title": 'An end-to-end model of active electrosensation',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12239031/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Çekiçbaş köpekbalığının geniş duyu yüzeyi',
        "category": 'Sensörler',
        "keywords": [
            'geniş alanda zayıf elektrik sinyali',
            'çok noktalı elektrik alan algılama',
            'su dibinde sensör tarama genişliği',
        ],
        "mechanism": 'Geniş baş, elektrik alanı algılayan reseptörleri geniş bir bölgeye yayar.',
        "solution": 'Geniş açıklıklı elektrot dizisi.',
        "pilot_test": 'Aynı algılayıcı sayısıyla tarama alanı ve konum hatasını ölçün.',
        "source_title": 'Head morphology and electrosensory pore distribution of carcharhinid and sphyrnid sharks',
        "source_url": 'https://citeseerx.ist.psu.edu/document?doi=9346813ccbf2419511abbceacfe69c699d14e1cd&repid=rep1&type=pdf',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Köstebeğin yıldız biçimli dokunma organı',
        "category": 'Sensörler',
        "keywords": [
            'dar alanda hızlı yüzey tanıma',
            'çok uçlu temas algılayıcı',
            'küçük parçayı dokunarak ayırt etmek',
        ],
        "mechanism": 'Burundaki radyal uzantılar çok sayıda mekanik algılayıcı taşır.',
        "solution": 'Yıldız biçimli yumuşak temas sensörü.',
        "pilot_test": 'Karışık küçük parçaları tanıma süresini ve hata oranını ölçün.',
        "source_title": 'A nose that looks like a hand and acts like an eye: the unusual mechanosensory system of the star-nosed mole',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/10555270/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Kum akrebinin titreşimle yön bulması',
        "category": 'Sensörler',
        "keywords": [
            'zemin titreşiminden kaynak yönü',
            'kum zeminde arıza konumu',
            'dağınık titreşim sensörleriyle yön',
        ],
        "mechanism": 'Ayaklardaki algılayıcılar zeminden yayılan titreşimlerin varış farkına duyarlıdır.',
        "solution": 'Çevreye dağılmış titreşim sensörleriyle kaynak yönü kestirimi.',
        "pilot_test": 'Bilinen kaynak açılarında konum ve yön hatasını ölçün.',
        "source_title": 'Compressional and surface waves in sand: used by desert scorpions to locate prey',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/17783246/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Örümceğin yarık biçimli gerinim organı',
        "category": 'Sensörler',
        "keywords": [
            'çok küçük gövde gerinimini algılamak',
            'ince kiriş çatlağı erken sinyal versin',
            'yarık geometrisi gerinim sensörü',
        ],
        "mechanism": 'Kutikuladaki dar yarıklar mekanik şekil değişimini duyusal sinyale bağlar.',
        "solution": 'Yarık dizili ince gerinim sensörü.',
        "pilot_test": 'Artan yük altında en küçük algılanabilir gerinimi ve tekrar edilebilirliği ölçün.',
        "source_title": 'The spider cuticle: a remarkable material toolbox for functional diversity',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC8326826/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Çöl kınkanatlısının yansıtıcı beyaz pulları',
        "category": 'Optik Yüzeyler',
        "keywords": [
            'titanyum pigment kullanmadan beyaz yüzey',
            'ince beyaz tabaka opak değil',
            'az malzemeyle opak beyaz',
        ],
        "mechanism": 'Cyphochilus pullarındaki düzensiz ince kitin ağı ışığı güçlü biçimde saçar.',
        "solution": 'Düşük kütleli gözenekli beyaz optik tabaka.',
        "pilot_test": 'Eş kütlede yayınık yansıma ve opaklığı ölçün.',
        "source_title": 'Structural optimization for broadband scattering in several ultra-thin white beetle scales',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/20676179/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Cam kanatlı kelebeğin düzensiz nano çıkıntıları',
        "category": 'Optik Yüzeyler',
        "keywords": [
            'saydam etiket farklı açılarda parlıyor',
            'şeffaf sensör kapağında geniş açı yansıma',
            'düzensiz nano doku saydamlık',
        ],
        "mechanism": 'Cam kanat bölgelerindeki düzensiz nano çıkıntılar geniş açı aralığında yansımayı azaltır.',
        "solution": 'Geniş açılı yansıma azaltan saydam film.',
        "pilot_test": 'Farklı açılarda yansıma ve sislenme değerini ölçün.',
        "source_title": 'The role of random nanostructures for the omnidirectional anti-reflection properties of the glasswing butterfly',
        "source_url": 'https://www.nature.com/articles/ncomms7909',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Mavi ışık yansıtan Selaginella yaprağı',
        "category": 'Optik Yüzeyler',
        "keywords": [
            'ince film maviyi seçici yansıtsın',
            'yaprak benzeri optik kaplama',
            'ince yüzeyde mavi parıltı',
        ],
        "mechanism": 'Selaginella willdenowii yapraklarının bazı bölgelerinde çok katmanlı kutikula renkli yansıma üretir.',
        "solution": 'İnce ve seçici yansıtıcı yüzey katmanı.',
        "pilot_test": 'Spektrometreyle yansıma tepe dalga boyunu belirleyin.',
        "source_title": 'Physical phenomena of thin surface layers',
        "source_url": 'https://api.repository.cam.ac.uk/server/api/core/bitstreams/6f4c9462-3a03-482f-8181-5a2568e2b847/content',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Sivrisinek gözünün buğuya dirençli mikro yapısı',
        "category": 'Optik Yüzeyler',
        "keywords": [
            'optik sensör nemde görüntüyü kaybediyor',
            'göz benzeri küçük mercek dizisi',
            'mikro mercek yüzeyi buğulanıyor',
        ],
        "mechanism": 'Bileşik göz, mikro ölçekli fasetleri daha küçük yüzey özellikleriyle bir araya getirir.',
        "solution": 'Mikro mercek dizisinde hiyerarşik yüzey dokusu.',
        "pilot_test": 'Nem döngüsünde görüntü kontrastını ve optik yansımayı izleyin.',
        "source_title": 'The dry-style antifogging properties of mosquito compound eyes and artificial analogues prepared by soft lithography',
        "source_url": 'https://doi.org/10.1002/adma.200601946',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Dulavratotu meyvesinin mikro kancaları',
        "category": 'Yeniden Kullanılabilir Bağlantı',
        "keywords": [
            'koli bant olmadan kapanmalı',
            'paket defalarca açılsın',
            'tek kullanımlık bant yerine kancalı kapama',
        ],
        "mechanism": 'Kancalı çıkıntılar liflere mekanik olarak takılır.',
        "solution": 'Değiştirilebilir lif şeridine takılan ambalaj kapağı.',
        "pilot_test": 'Açma kuvvetini ve yüz çevrim sonrası tutuşu ölçün.',
        "source_title": 'Who came up with the idea for Velcro?',
        "source_url": 'https://www.loc.gov/everyday-mysteries/technology/item/who-came-up-with-the-idea-for-velcro/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Güneşgülü bitkisinin yapışkan damlaları',
        "category": 'Islak Bağlantı',
        "keywords": [
            'ince parçacıkları damlayla yakalamak',
            'küçük yüzeyde seçici yapışkan nokta',
            'sıvı damlası uzayarak parçayı tutsun',
        ],
        "mechanism": 'Drosera yapraklarının tüy uçlarındaki viskoelastik salgı, uzayabilen küçük yapışkan damlalar oluşturur.',
        "solution": 'Kuru ince parçacıkları yakalamak için ayrı damlalar taşıyan mikro yüzey.',
        "pilot_test": 'Aynı temas süresinde tutulan parçacık kütlesini ve damlanın kopma uzamasını ölçün.',
        "source_title": 'Microrheometry of sub-nanoliter biopolymer samples: non-Newtonian flow phenomena of carnivorous plant mucilage',
        "source_url": 'https://web.mit.edu/nnf/publications/GHM172.pdf',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Fil derisinin su tutan çatlakları',
        "category": 'Su Yönetimi',
        "keywords": [
            'soğutma yüzeyindeki su hemen akıyor',
            'pürüzlü yüzeyde su filmi tutmak',
            'ıslak soğutma yüzeyi çabuk kuruyor',
        ],
        "mechanism": 'Fil derisindeki ince çatlaklar suyun yüzeyde tutulmasına katkıda bulunur.',
        "solution": 'Buharlaşmalı soğutma paneli için mikro kanallı yüzey.',
        "pilot_test": 'Eş miktarda suyla yüzey sıcaklığı ve kuruma süresini ölçün.',
        "source_title": 'Locally-curved geometry generates bending cracks in the African elephant skin',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/30279508/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Dikenli şeytan kertenkelesinin kılcal kanalları',
        "category": 'Su Yönetimi',
        "keywords": [
            'zemindeki damlayı yukarı taşımak',
            'pompasız suyu kenara almak',
            'kılcal kanalla dağınık su toplamak',
        ],
        "mechanism": 'Deri pulları arasındaki kanallar suyu kapiler etkiyle taşır.',
        "solution": 'Kılcal ağla sıvıyı bir toplama noktasına alan yüzey.',
        "pilot_test": 'Aynı su hacminde aktarım hızı ve erişilen mesafeyi ölçün.',
        "source_title": 'Cutaneous Water Acquisition by the Thorny Devil (Moloch horridus: Agamidae) | JSTOR',
        "source_url": 'https://www.jstor.org/stable/1565146?read-now=1',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Phrynosoma kertenkelesinin yönlü su kanalları',
        "category": 'Su Yönetimi',
        "keywords": [
            'yüzeyde su tek tarafa ilerlesin',
            'damla geri yayılıyor',
            'kanalsız pompasız yönlü sıvı aktarımı',
        ],
        "mechanism": 'Bazı boynuzlu kertenkelelerde kanal geometrisi sıvının yönlü yayılmasını destekler.',
        "solution": 'Asimetrik kanallarla pasif yönlü sıvı hattı.',
        "pilot_test": 'İleri ve geri yönde aynı sürede alınan mesafeyi ölçün.',
        "source_title": 'Directional, passive liquid transport: the Texas horned lizard as a model for a biomimetic ‘liquid diode’',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4535411/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Çöl otunun oluklu sis toplama yaprağı',
        "category": 'Su Hasadı',
        "keywords": [
            'sis ağı bitki yaprağı gibi suyu taşısın',
            'sisten toplanan damla kenara akmıyor',
            'oluklu yaprakla sis hasadı',
        ],
        "mechanism": 'Çöl otunun yaprak yüzeyi ve olukları sis damlalarının toplanıp akmasına katkı verir.',
        "solution": 'Boyuna oluklu ince sis toplama şeridi.',
        "pilot_test": 'Birbirinden farklı oluk kesitlerinde birim alan başına suyu ölçün.',
        "source_title": 'Leaf surface structures enable the endemic Namib desert grass Stipagrostis sabulicola to irrigate itself with fog water',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/22356817/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Tropik yaprakların damlama ucu',
        "category": 'Su Yönetimi',
        "keywords": [
            'ıslak kenarda damla asılı kalıyor',
            'yaprak ucu gibi suyu bırakmak',
            'damlatma ucunda su birikiyor',
        ],
        "mechanism": 'Sivri yaprak ucu sıvının yüzeyden ayrıldığı dar bir nokta oluşturur.',
        "solution": 'İnce ucu değiştirilebilir pasif tahliye kenarı.',
        "pilot_test": 'Farklı eğimlerde damlanın ayrılma hacmini ve süreyi ölçün.',
        "source_title": 'An ecological perspective on water shedding from leaves',
        "source_url": 'https://academic.oup.com/jxb/article/73/4/1176/6417382',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Lahana yaprağının mumsu su iticiliği',
        "category": 'Islak Yüzeyler',
        "keywords": [
            'yeşil sebze yüzeyi ıslanmıyor',
            'mumsu gıda yüzeyinde damla yayılması',
            'doğal mumlu yüzeyin su itmesi',
        ],
        "mechanism": 'Yaprak üstü mum kristalleri yüzeyin ıslanma davranışını etkiler.',
        "solution": 'Gözenekli koruyucu numune için mumlu yüzey örneği.',
        "pilot_test": 'Temas açısını ve sürtünme sonrası su iticiliğini ölçün.',
        "source_title": 'Plant cuticles: Multifunctional interfaces',
        "source_url": 'https://www.esalq.usp.br/lepse/imgs/conteudo_thumb/The-Evolution-of-Plant-Physiology-by-Hensley---Poole--2004-.pdf',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Pirinç yaprağının yönlü ıslanabilirliği',
        "category": 'Islak Yüzeyler',
        "keywords": [
            'damla yalnızca uzunlamasına aksın',
            'dokuya göre damla yana kaçıyor',
            'yönlü ıslanabilirlik ölçümü',
        ],
        "mechanism": 'Yaprak yüzeyindeki yönlü mikro yapı damla hareketini yönlere göre değiştirir.',
        "solution": 'Yönlü mikro oluklu sıvı kontrol yüzeyi.',
        "pilot_test": 'Yatay ve dik yönde damlanın kayma açısını ölçün.',
        "source_title": 'Fabrication of biomimetic anisotropic super-hydrophobic surface with rice leaf-like structures by femtosecond laser',
        "source_url": 'https://www.sciencedirect.com/science/article/pii/S092534672031079X',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Kelebek kanadının yönlü damla tutuşu',
        "category": 'Islak Yüzeyler',
        "keywords": [
            'damla ters yönde yüzeye yapışıyor',
            'yönlü damla bırakma sensörü',
            'doku yönüne göre damla tutuşu',
        ],
        "mechanism": 'Bazı kanat pullarında yönlü düzen, damlanın farklı yönlerde farklı kuvvetle tutulmasına neden olur.',
        "solution": 'Damlaları tek yönde daha kolay serbest bırakan yüzey.',
        "pilot_test": 'İki yönde kopma kuvvetini ölçün.',
        "source_title": 'Directional adhesion of superhydrophobic butterfly wings',
        "source_url": 'https://pubs.rsc.org/en/content/articlelanding/2007/sm/b612667g/unauth',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Sürahi bitkisi iç duvarının mumsu pulları',
        "category": 'Yüzey Tasarımı',
        "keywords": [
            'kuru yüzeyde tutunmayı azaltmak',
            'ince mumla düşük tutuş',
            'kuruyken kaygan mikro doku',
        ],
        "mechanism": 'Bazı Nepenthes türlerinde iç duvardaki mum kristalleri böceklerin kuru yüzeye tutunmasını azaltır.',
        "solution": 'Kuru koşullarda düşük temas tutuşu veren mikro dokulu numune.',
        "pilot_test": 'Standart temas ayağında kuru sürtünme kuvvetini ölçün.',
        "source_title": 'Slippery surfaces of pitcher plants: Nepenthes wax crystals minimize insect attachment via microscopic surface roughness',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/20228348/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Yumuşakça Pinna’nın ince tutunma lifleri',
        "category": 'Kavrama ve Robotik',
        "keywords": [
            'ıslak bağlantıda çok ince yük taşıyan lif',
            'ince bağlantı suda kopuyor',
            'deniz ortamında lifli ankraj',
        ],
        "mechanism": 'Pinna türleri su altında tutunmak için çok sayıda ince byssus lifi kullanır.',
        "solution": 'Tek bağlantı yerine küçük lif demetli ankraj numunesi.',
        "pilot_test": 'Tek lif ve demet halinde çekme kuvvetini ölçün.',
        "source_title": 'The byssus threads of Pinna nobilis: A histochemical and ultrastructural study',
        "source_url": 'https://www.ejh.it/index.php/ejh/article/view/2779',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Kum kale solucanının iki bileşenli yapıştırıcısı',
        "category": 'Islak Bağlantı',
        "keywords": [
            'suda mineral taneleri birleştirmek',
            'ıslak parçacıklarla yerinde bağ oluşsun',
            'su içinde akışkan tutkal ayrılsın',
        ],
        "mechanism": 'Solucan mineral tanelerini suda birleştiren salgı ile tüp inşa eder.',
        "solution": 'Su altında mineral taneleri birleştirmeyi amaçlayan iki aşamalı bağlayıcı.',
        "pilot_test": 'Sertleşme süresi ve kesme dayanımını ölçün.',
        "source_title": 'Localization of the bioadhesive precursors of the sandcastle worm, Phragmatopoma californica (Fewkes)',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/22189779/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Deniz palamudunun sualtı çimentosu',
        "category": 'Islak Bağlantı',
        "keywords": [
            'deniz sensörü bağlantısı su altında ayrılıyor',
            'ıslak yüzeyde kalıcı bağ',
            'deniz taşı üstünde bağlayıcı testi',
        ],
        "mechanism": 'Yetişkin barnacle, ıslak yüzeye bağlanan proteinli çimento salgılar.',
        "solution": 'Islak mineral yüzeyler için protein esinli bağlayıcı numune.',
        "pilot_test": 'Daldırma çevrimi sonrası yapışma dayanımını ölçün.',
        "source_title": '[The adhesion mechanism of barnacle and its cement proteins: a review]',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/36593188/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'İpekböceğinin lif oluşturan kanalı',
        "category": 'Malzeme ve Üretim',
        "keywords": [
            'lif üretirken çözelti düzensiz katılaşıyor',
            'su bazlı ince lif çekimi',
            'akış kanalı boyunca lifleşme',
        ],
        "mechanism": 'İpek kanalındaki akış ve kimyasal ortam fibroinin lif hâline gelmesine katkı verir.',
        "solution": 'Akış hızı ve ortamı kademeli değişen lif çekim kanalı.',
        "pilot_test": 'Çekilen lifin çap dağılımını ve çekme davranışını ölçün.',
        "source_title": 'A brief review on the mechanisms and approaches of silk spinning-inspired biofabrication',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10512026/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Sepet süngerinin katmanlı silika lifleri',
        "category": 'Malzeme Dayanımı',
        "keywords": [
            'cam lif eğilince bir anda kırılıyor',
            'mineral lifte ince ara katman',
            'cam elyafta çatlak ilerlemesi',
        ],
        "mechanism": 'Cam süngerinin silika iğneciklerinde eş merkezli mineral ve organik katmanlar bulunur.',
        "solution": 'Eş merkezli katmanlı kırılgan lif prototipi.',
        "pilot_test": 'Kademeli eğmede ilk hasar ve kopma deformasyonunu ölçün.',
        "source_title": 'Skeleton of Euplectella sp.: structural hierarchy from the nanoscale to the macroscale',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/16002612/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Deniz hıyarının sıvı tüplerle tutunması',
        "category": 'Islak Bağlantı',
        "keywords": [
            'temas eden ıslak ağ yapışsın',
            'suda serilen yapışkan lif',
            'çekince yayılan ağın tutuşu',
        ],
        "mechanism": 'Bazı deniz hıyarları savunmada yapışkan Cuvier tüpleri çıkarır.',
        "solution": 'Su içinde açılıp standart yüzeye tutunan deneysel lif ağı.',
        "pilot_test": 'Ağ açılma süresi ile ıslak yüzeyden ayrılma kuvvetini ölçün.',
        "source_title": 'Maintaining the line of defense: regeneration of Cuvierian tubules in the sea cucumber Holothuria forskali (Echinodermata, Holothuroidea)',
        "source_url": 'https://www.journals.uchicago.edu/doi/pdf/10.2307/1542802',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Kunduz kesici dişinin demirli ön minesi',
        "category": 'Malzeme Dayanımı',
        "keywords": [
            'kesici ucun yalnızca ön yüzü aşınmasın',
            'kenarda metalce zengin tabaka',
            'kesici kenar uzun süre kalsın',
        ],
        "mechanism": 'Kesici dişlerin ön mine bölgesi demirce zengindir ve farklı kimyasal özellikler gösterir.',
        "solution": 'Ön yüzü takviyeli asimetrik kesici uç numunesi.',
        "pilot_test": 'Aşındırma çevrimlerinde kenar yarıçapını ve kütle kaybını izleyin.',
        "source_title": 'Electron microprobe analysis of iron content of incisor enamel in some species of rodentia',
        "source_url": 'https://www.sciencedirect.com/science/article/pii/0003996974902179',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Kemirgen kesici dişinin kendi kendini bileyen kesiti',
        "category": 'Malzeme Dayanımı',
        "keywords": [
            'kesici uç kullanımda köreliyor',
            'kendi kendini bileyen katman',
            'asimetrik aşınmayla keskinlik koruma',
        ],
        "mechanism": 'Mine ve dentin farklı hızda aşınarak kesici kenarın korunmasına katkı verir.',
        "solution": 'Farklı aşınma hızına sahip iki katmanlı kesici uç.',
        "pilot_test": 'Aşınma çevrimlerinde kenar geometrisi ve kesme kuvvetini ölçün.',
        "source_title": 'WHO training document on rodent identification and biology',
        "source_url": 'https://iris.who.int/bitstream/handle/10665/61081/WHO_VBC_87.949_eng.pdf',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Vatoz derisinin bölgesel dentikül dağılımı',
        "category": 'Yüzey Tasarımı',
        "keywords": [
            'yüzeyde bölgeye göre sürtünme değişsin',
            'farklı yönlerde sert yüzey çıkıntıları',
            'tek tip dokunun temas kontrolü zayıf',
        ],
        "mechanism": 'Bazı vatozların derisinde bölgeye göre değişen küçük dentiküller bulunur.',
        "solution": 'Bölgesel olarak yönü ve sıklığı değişen sert mikro doku.',
        "pilot_test": 'Yönlere ve bölgelerine göre sürtünme katsayısını haritalayın.',
        "source_title": 'Comparison of vertebrate skin structure at class level: A review',
        "source_url": 'https://anatomypubs.onlinelibrary.wiley.com/doi/10.1002/ar.24908',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Kanguru sıçanının burun ısı ve nem değişimi',
        "category": 'Isı ve Nem Yönetimi',
        "keywords": [
            'egzoz havasındaki nem kayboluyor',
            'solunum benzeri nem geri kazanımı',
            'sıcak hava çıkışından su geri almak',
        ],
        "mechanism": 'Kanguru sıçanı, burun geçişlerinde solunum havasından su kaybını azaltabilir.',
        "solution": 'Çıkış havasından nemi geri kazanmayı hedefleyen geçiş kanalı.',
        "pilot_test": 'Giriş çıkış nemi, sıcaklık ve basınç kaybını ölçün.',
        "source_title": 'Turbinal bones are still one of the last frontiers of the tetrapod skull: hypotheses, challenges and perspectives',
        "source_url": 'https://onlinelibrary.wiley.com/doi/full/10.1111/brv.13122',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Çöl salyangozunun geçici ağız kapağı',
        "category": 'Isı ve Nem Yönetimi',
        "keywords": [
            'havalandırma açıkken nem kaçıyor',
            'kurumada geçici koruma kapağı',
            'geçici su buharı bariyeri',
        ],
        "mechanism": 'Bazı kara salyangozları kurak dönemde kabuk ağzında epifram oluşturur.',
        "solution": 'Geçici ve kontrollü geçirgen nem kaybı bariyeri.',
        "pilot_test": 'Aynı nem farkında buhar geçişi ve çıkarma kuvvetini ölçün.',
        "source_title": 'Snails in the sun: Strategies of terrestrial gastropods to cope with hot and dry conditions',
        "source_url": 'https://onlinelibrary.wiley.com/doi/full/10.1002/ece3.5607',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Yaprak stomalarının ayarlanabilir açıklığı',
        "category": 'Isı ve Nem Yönetimi',
        "keywords": [
            'hava geçişi nem kaybına göre ayarlansın',
            'pasif ayarlı küçük havalandırma',
            'nem hassas açıklık kontrolü',
        ],
        "mechanism": 'Bekçi hücrelerinin turgor değişimi yapraktaki açıklığın boyutunu düzenler.',
        "solution": 'Nem koşullarına göre açıklığı değişen mikro havalandırma.',
        "pilot_test": 'Nem basamaklarında açıklık alanı ve hava akışını ölçün.',
        "source_title": 'Modelling stomatal mechanics: a critical review',
        "source_url": 'https://nph.onlinelibrary.wiley.com/doi/10.1111/nph.70826',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Çam iğnesinin içe gömülü stomaları',
        "category": 'Isı ve Nem Yönetimi',
        "keywords": [
            'hava deliğinde buhar kaybını azaltmak',
            'yüzey içine gömülü havalandırma kanalı',
            'kuru ortamda açıklık fazla buhar geçiriyor',
        ],
        "mechanism": 'Bazı çam iğnelerinde stomalar yüzeye göre içe gömülüdür.',
        "solution": 'İçe gömülü açıklıklardan oluşan hava geçiş plakası.',
        "pilot_test": 'Gaz geçişini ve su buharı kaybını birlikte ölçün.',
        "source_title": 'Conifer Needle Epidermal Imprints for Stomatal Size and Density Measurements',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC13691621/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Zeytin yaprağının alt yüzey tüyleri',
        "category": 'Isı ve Nem Yönetimi',
        "keywords": [
            'açık hava paneli rüzgârda kuruyor',
            'gölgeli mikro tüylerle su kaybı',
            'tüylü yüzeyde buharlaşma deneyi',
        ],
        "mechanism": 'Zeytin yaprağının altında yoğun örtü tüyleri bulunur.',
        "solution": 'Korunan yüzeyde ince lif örtüsü ile yerel mikro ortam.',
        "pilot_test": 'Aynı hava hızında su kaybını ve yüzey sıcaklığını ölçün.',
        "source_title": 'Horticultural Reviews, volume 31: Olive leaf morphology',
        "source_url": 'https://uodiyala.edu.iq/uploads/PDF%20ELIBRARY%20UODIYALA/EL34/Horticultural%20Reviews%20Volume%2031.pdf',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Kutupsal balığın buz bağlayan proteinleri',
        "category": 'Soğuk Zincir',
        "keywords": [
            'donmuş numunede buz kristalleri büyüyor',
            'dondurma çözme kristal hasarı',
            'buz kristali büyümesini yavaşlatmak',
        ],
        "mechanism": 'Antifriz glikoproteinleri buz yüzeyleriyle etkileşerek kristal büyümesini etkiler.',
        "solution": 'Laboratuvar ölçeğinde buz büyümesini kontrol eden katkı taraması.',
        "pilot_test": 'Mikroskop altında kristal boyutu dağılımını karşılaştırın.',
        "source_title": 'Glycoproteins as biological antifreeze agents in antarctic fishes',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/5574522/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Kar piresinin antifriz proteini',
        "category": 'Soğuk Zincir',
        "keywords": [
            'ince su filminde donmayı geciktirmek',
            'soğuk sensörde buz büyümesi',
            'protein benzeri buz bağlayıcı deney',
        ],
        "mechanism": 'Kar piresinde tanımlanan proteinler buz kristali büyümesini etkiler.',
        "solution": 'Soğukta çalışan yüzey için buz oluşumu deney numunesi.',
        "pilot_test": 'Aynı soğutma programında donma başlangıcı ve buz yayılımını ölçün.',
        "source_title": 'Glycine-rich antifreeze proteins from snow fleas',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/16239469/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'İmparator pengueninin bölgesel ısı kaybı',
        "category": 'Isı ve Enerji Yönetimi',
        "keywords": [
            'yalıtımlı gövdenin uçları ısı kaçırıyor',
            'koruyucu kaplamada sıcaklık farklılıkları',
            'dış yüzeyde bölgesel ısı kaybı ölçmek',
        ],
        "mechanism": 'Isıl görüntüleme, yoğun tüylü gövde ile ayak ve kanat gibi bölgelerin farklı ısı alışverişi gösterdiğini ortaya koyar.',
        "solution": 'Muhafazanın farklı bölgelerine ayrı yalıtım kalınlıkları uygulayan bir numune.',
        "pilot_test": 'Aynı giriş gücünde termal kamera ile yüzey sıcaklıklarını ve toplam enerji kaybını karşılaştırın.',
        "source_title": 'Emperor penguin body surfaces cool below air temperature',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC3645025/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Büyük kulaklı tavşanın ısı yayan kulağı',
        "category": 'Isı ve Enerji Yönetimi',
        "keywords": [
            'cihaz ısısını kanatçıkla atmak',
            'ısıyı büyük ince yüzeyle yaymak',
            'gövde yanına ısı yayıcı panel',
        ],
        "mechanism": 'Geniş ve damarlı kulak yüzeyi belirli koşullarda ısı alışverişi sağlar.',
        "solution": 'Akışkanla beslenen geniş ince ısı yayma paneli.',
        "pilot_test": 'Aynı güçte iç sıcaklık ve panel ısı akısını ölçün.',
        "source_title": 'Jackrabbit ears: surface temperatures and vascular responses',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/982027/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Pieris kelebeğinin yönelimli güneşlenmesi',
        "category": 'Isı ve Enerji Yönetimi',
        "keywords": [
            'güneş panelinin açısı sıcaklığa göre değişsin',
            'güneşte pasif yönelimle ısınma',
            'hareketli güneşlenen yüzey',
        ],
        "mechanism": 'Pieris kelebekleri kanat açılarını değiştirerek ışınımın gövdeye ulaşmasını etkileyebilir.',
        "solution": 'Farklı açılara dönebilen hafif güneş yüzeyi deneyi.',
        "pilot_test": 'Işınım sabitken ısınma hızı ve denge sıcaklığını ölçün.',
        "source_title": 'Thermal ecology of Pieris butterflies (Lepidoptera: Pieridae): a new mechanism of behavioral thermoregulation',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/28310796/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Kutup ayısının yalıtkan kürk yapısı',
        "category": 'Isı ve Enerji Yönetimi',
        "keywords": [
            'hafif yalıtım katmanı rüzgârda soğuyor',
            'lifli yalıtımda hava hapsi',
            'gözenekli kürk benzeri yalıtım',
        ],
        "mechanism": 'Kürk lifleri arasında tutulan hava ısıl yalıtıma katkı verir.',
        "solution": 'Hava tutan çok katmanlı lifli yalıtım numunesi.',
        "pilot_test": 'Farklı rüzgâr hızlarında ısı akısını ölçün.',
        "source_title": 'Polar bear thermoregulation: Effect of oil on the insulative properties of fur',
        "source_url": 'https://www.sciencedirect.com/science/article/pii/0306456582900250',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Kutup tilkisinin mevsimsel kürk yoğunluğu',
        "category": 'Isı ve Enerji Yönetimi',
        "keywords": [
            'yalıtım kalınlığı mevsime göre değişsin',
            'sökülebilir kış yalıtımı',
            'iki farklı mevsim için modüler lif katmanı',
        ],
        "mechanism": 'Kürk kalınlığı ve yalıtım özellikleri mevsime göre değişir.',
        "solution": 'Mevsime göre eklenip çıkarılabilen lifli muhafaza.',
        "pilot_test": 'Farklı katman sayılarında enerji kaybı ve kütleyi karşılaştırın.',
        "source_title": 'Adaptation by the Arctic Fox (Alopex lagopus) to the Polar Winter',
        "source_url": 'https://journalhosting.ucalgary.ca/index.php/arctic/article/view/64583',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Misk öküzünün ince qiviut alt kürkü',
        "category": 'Isı ve Enerji Yönetimi',
        "keywords": [
            'ince lifli iç yalıtım tabakası',
            'kalın dış kabuk yerine yumuşak astar',
            'düşük kütlede sıcak astar',
        ],
        "mechanism": 'Misk öküzünde ince alt kürk daha kaba dış kılların altında yer alır.',
        "solution": 'Kaba dış koruma ve ince iç astardan iki katman.',
        "pilot_test": 'Eş kütlede ısıl direnç ve sıkıştırma sonrası toparlanmayı ölçün.',
        "source_title": 'Fiber characteristics of qiviut and guard hair from wild muskoxen (Ovibos moschatus)',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/11465352/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Küstüm otunun hidrolik yaprak mafsalı',
        "category": 'Pasif Mekanizmalar',
        "keywords": [
            'dokununca hızlı kapanan yumuşak mafsal',
            'sıvı basıncıyla yaprak gibi kapanma',
            'esnek kapak temasla hareket etsin',
        ],
        "mechanism": 'Pulvinus dokusunda hızlı su ve iyon hareketleri turgoru değiştirir.',
        "solution": 'Düşük basınçlı sıvı haznesiyle kapanan yumuşak mafsal.',
        "pilot_test": 'Girdi sinyalinden kapanmaya kadar gecikmeyi ve çevrim ömrünü ölçün.',
        "source_title": 'Mechanical Signaling in the Sensitive Plant Mimosa pudica L',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC7284940',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Su mercimeğinin suda besin alımı',
        "category": 'Su Arıtma ve Döngüsellik',
        "keywords": [
            'suda azot ve fosfor yükünü azaltmak',
            'atık sudan besin geri kazanımı',
            'su bitkisiyle besin toplama',
        ],
        "mechanism": 'Su mercimeği çözünmüş besinleri büyüyen biyokütlesine alabilir.',
        "solution": 'Kontrollü küçük su arıtma pilotunda hasat edilebilir bitki tabakası.',
        "pilot_test": 'Başlangıç ve bitiş azot ve fosfor konsantrasyonlarını ölçün.',
        "source_title": 'Growth and nutrient removal efficiency of duckweed (lemna minor) from synthetic and dumpsite leachate under artificial and natural conditions',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6711526/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Mesane otu tuzağının hızlı emişi',
        "category": 'Akış ve Dozaj',
        "keywords": [
            'küçük sıvı örneğini aniden çekmek',
            'vakumla hızlı örnek yakalama',
            'esnek hazne küçük kapakla açılsın',
        ],
        "mechanism": 'Tuzağın esnek duvarı basınç farkını depolar ve kapak açılınca su içeri girer.',
        "solution": 'Önceden yüklenen esnek hazneli numune alıcı.',
        "pilot_test": 'Açılmadan doluma kadar süreyi ve çekilen hacmi ölçün.',
        "source_title": 'Mechanical model of the ultrafast underwater trap of Utricularia',
        "source_url": 'https://journals.aps.org/pre/abstract/10.1103/PhysRevE.83.021911',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Şeytan hıyarının basınçlı tohum çıkışı',
        "category": 'Akış ve Dozaj',
        "keywords": [
            'depolanan basınçla küçük parçayı bırakmak',
            'bitki gibi basınçlı atış düzeneği',
            'akışkanla aralıklı parça çıkarma',
        ],
        "mechanism": 'Olgun meyve basınç altında tohumları sıvı jetiyle dışarı çıkarır.',
        "solution": 'Kapalı bir deneyde basınçla tek doz bırakan hazne.',
        "pilot_test": 'Basınca göre doz kütlesini ve çıkış gecikmesini ölçün.',
        "source_title": 'Uncovering the mechanical secrets of the squirting cucumber',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/39586000/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Kına çiçeğinin gerilimli tohum kapsülü',
        "category": 'Pasif Mekanizmalar',
        "keywords": [
            'tetiklenince açılan elastik paket',
            'yay koymadan hızlı açılan kapak',
            'paket kenarları kıvrılıp ayrılsın',
        ],
        "mechanism": 'Meyve valfleri depolanan elastik enerjiyle hızla kıvrılır.',
        "solution": 'Tetikle açılan, ön gerilimli ince kapak şeridi.',
        "pilot_test": 'Açılma süresi, tetik kuvveti ve çevrim tutarlılığını ölçün.',
        "source_title": 'Finessing the fracture energy barrier in ballistic seed dispersal',
        "source_url": 'https://public.websites.umich.edu/~rddeegan/PDF/Exploding_Seeds.pdf',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Cadı fındığının sıkışarak fırlatan tohum kabuğu',
        "category": 'Pasif Mekanizmalar',
        "keywords": [
            'küçük parçaları sıkıştırıp bırakmak',
            'mandal bırakınca parça fırlasın',
            'sıkma ile pasif parça çıkışı',
        ],
        "mechanism": 'Kuruyan kapsül tohumu sıkar ve bir noktada serbest bırakır.',
        "solution": 'Düşük enerjili kontrollü parça çıkarma mandalı.',
        "pilot_test": 'Çıkış kuvvetini ve parçanın yerleşme hatasını ölçün.',
        "source_title": 'A seed flying like a bullet: ballistic seed dispersal in Chinese witch-hazel (Hamamelis mollis OLIV., Hamamelidaceae)',
        "source_url": 'https://royalsocietypublishing.org/doi/pdf/10.1098/rsif.2019.0327',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Banksia’nın ısıyla açılan odunsu meyvesi',
        "category": 'Tarım ve Pasif Mekanizmalar',
        "keywords": [
            'sıcaklık eşiğinde mekanik kapak açılsın',
            'ısınınca kuru tohum kabı açılması',
            'elektriksiz sıcaklıkla açılan kapak',
        ],
        "mechanism": 'Bazı Banksia kapsüllerinde yüksek sıcaklık tohum bırakmaya olanak veren açılmayı tetikler.',
        "solution": 'Kontrollü sıcaklıkta açılan pasif numune haznesi.',
        "pilot_test": 'Sıcaklık basamaklarında açılma eşiğini ve süreyi ölçün.',
        "source_title": 'Temperature-induced self-sealing capability of Banksia follicles',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/29925581/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Bauhinia bitkisinin burulan baklası',
        "category": 'Tarım ve Pasif Mekanizmalar',
        "keywords": [
            'kuruyunca iki şerit ters yöne burulsun',
            'nemle çalışan helisel şerit',
            'iki katlı kuru şeritte burulma',
        ],
        "mechanism": 'Bauhinia baklasının farklı yönlenmiş katmanları kuruma sırasında burulur.',
        "solution": 'Nem değişiminden burulma üreten iki katmanlı şerit.',
        "pilot_test": 'Nem oranına karşı üretilen dönme açısını ve momenti ölçün.',
        "source_title": 'Geometry and mechanics in the opening of chiral seed pods',
        "source_url": 'https://doi.org/10.1126/science.1203874',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Cardamine baklasının asimetrik liflerle açılması',
        "category": 'Tarım ve Pasif Mekanizmalar',
        "keywords": [
            'kuruyan kabuk dikişten açılıyor',
            'kuru kapsülde dikiş gerilimi',
            'kurumayla ayrılan biyobazlı ambalaj',
        ],
        "mechanism": 'Cardamine hirsuta baklasında hücre biçimi ve asimetrik lignin dağılımı valfin hızla kıvrılıp ayrılmasına katkı verir.',
        "solution": 'Tek kenarından açılacak şekilde farklı bölgeleri sertleştirilmiş ince kapsül.',
        "pilot_test": 'Aynı nem döngüsünde ayrılma eşiğini ve dikiş sapmasını ölçün.',
        "source_title": 'Morphomechanical Innovation Drives Explosive Seed Dispersal',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4930488/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Bezelyenin temasla sarılan sülüğü',
        "category": 'Kavrama ve Robotik',
        "keywords": [
            'ince destek dokununca sarılsın',
            'temasla otomatik kablo tutma',
            'direğe kendiliğinden dolanan ince uç',
        ],
        "mechanism": 'Sülük temas sonrasında destek çevresine sarılabilir.',
        "solution": 'Temas sonrasında esnek bir şeridi destek çevresine yönlendiren tutucu.',
        "pilot_test": 'Desteğe temas ile tam sarım arasında süre ve kaymayı ölçün.',
        "source_title": 'Physiological studies on pea tendrils. XIII. Respiration is necessary for contact coiling',
        "source_url": 'https://profiles.wustl.edu/en/publications/physiological-studies-on-pea-tendrils-xiii-respiration-is-necessa/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Salatalık sülüğünün ters yönlü iki spirali',
        "category": 'Pasif Mekanizmalar',
        "keywords": [
            'uçları sabit şerit dönmeden kısalsın',
            'iki ters spiral ile esnek bağlantı',
            'sarılan hat iki uçta tork üretmesin',
        ],
        "mechanism": 'Sülükte farklı yönlerde iki helis oluşur ve arada yön değiştiren bölge bulunur.',
        "solution": 'Her iki ucu sabitken kısalan ters helisli bağlantı.',
        "pilot_test": 'Uç torkunu ve kısalma mesafesini aynı yükte ölçün.',
        "source_title": 'How the cucumber tendril coils and overwinds',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/22936777/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Yer fıstığının toprağa yönelen ginoforu',
        "category": 'Tarım ve Pasif Mekanizmalar',
        "keywords": [
            'ince uç toprağa doğru büyüsün',
            'yer çekimiyle yönlenen tarım işaretçisi',
            'toprak yüzeyine aşağı yönlü küçük prob',
        ],
        "mechanism": 'Yer fıstığının ginoforu aşağı yönelir ve meyve gelişimi toprak altında devam eder.',
        "solution": 'Aşağı yönlü büyüme fikrinden esinlenen yerçekimi yönelimli prob.',
        "pilot_test": 'Eğimli zeminde toprak giriş açısını ve hedef sapmasını ölçün.',
        "source_title": 'Deciphering the Proteome and Phosphoproteome of Peanut (Arachis hypogaea L.) Pegs Penetrating into the Soil',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC11765555/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Samanea ağacının geceleri katlanan yaprakları',
        "category": 'Pasif Mekanizmalar',
        "keywords": [
            'gece ışık olmayınca panel katlansın',
            'gündüz açık gece kapalı yaprak düzeneği',
            'ışık döngüsüne bağlı kapak',
        ],
        "mechanism": 'Yaprakçıkların konumu gün gece döngüsüyle değişebilir.',
        "solution": 'Işık döngüsüne göre katlanan küçük panel.',
        "pilot_test": 'Açık ve karanlık fazda açı farkını ve enerji gereksinimini ölçün.',
        "source_title": 'Bioorganic studies on the nyctinastic leaf-movement of plants',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12950841/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Ayçiçeğinin genç gövdeyle güneş takibi',
        "category": 'Isı ve Enerji Yönetimi',
        "keywords": [
            'güneşi izleyen küçük panel',
            'güneşe göre doğu batı yönelimi',
            'gün boyunca yavaş izleme düzeneği',
        ],
        "mechanism": 'Genç ayçiçeklerinde gövdenin iki yanındaki farklı büyüme günlük yönelime katkı verir.',
        "solution": 'Gün içi yönelimi değiştiren düşük hızlı güneş takip düzeneği.',
        "pilot_test": 'Sabit ve izleyen panellerin aynı günde enerji çıktısını ölçün.',
        "source_title": 'Circadian regulation of sunflower heliotropism, floral orientation, and pollinator visits',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/27493185/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Parazitik küskütün uçucu koku takibi',
        "category": 'Sensörler',
        "keywords": [
            'havada koku gradyanından kaynak bulmak',
            'gaz izini takip eden mini cihaz',
            'kokuya göre kaynak yönü seçimi',
        ],
        "mechanism": 'Küsküt fideleri bazı konakların uçucu kimyasal ipuçlarına doğru büyüme gösterebilir.',
        "solution": 'Çok noktada örnek alan gaz kaynağı konumlama düzeneği.',
        "pilot_test": 'Farklı hava akımlarında kaynak yönü hatasını ölçün.',
        "source_title": 'Volatile chemical cues guide host location and host selection by parasitic plants',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/17008532/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Söğüt kökünün su içindeki oksijen kanalları',
        "category": 'Su Arıtma ve Döngüsellik',
        "keywords": [
            'su altında kök çevresi oksijensiz kalıyor',
            'doymuş yatağa pasif hava yolu',
            'suya gömülü gözenekli havalandırma',
        ],
        "mechanism": 'Su basmasına uyum sağlayan bazı söğütlerde suya doygun ortamda yeni kökler oluşur ve hava taşıyan doku gelişebilir.',
        "solution": 'Doymuş yatakta gaz taşıyan gözenekli kanallar.',
        "pilot_test": 'Aynı akışta farklı derinliklerde çözünmüş oksijeni ölçün.',
        "source_title": 'Waterlogging effects on Salix viminalis',
        "source_url": 'https://doi.org/10.1017/S0269727000007648',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Pirinç kökünün hava taşıyan dokusu',
        "category": 'Su Arıtma ve Döngüsellik',
        "keywords": [
            'su altında havayı köke taşımak',
            'ıslak filtreye hava ileten kanal',
            'suya doygun yatakta oksijen dağılımı',
        ],
        "mechanism": 'Pirinç kökündeki aerenkima hava taşınmasına olanak sağlar.',
        "solution": 'Suya doygun filtreye uzanan pasif hava kanalı prototipi.',
        "pilot_test": 'Kanal uzunluğuna göre oksijen dağılımını ölçün.',
        "source_title": 'Aerenchyma and an Inducible Barrier to Radial Oxygen Loss Facilitate Root Aeration in Upland, Paddy and Deep‐water Rice (Oryza sativa L.)',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4795684/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Mangrovun tuz süzen kökleri',
        "category": 'Su Arıtma ve Döngüsellik',
        "keywords": [
            'tuzlu sudan kök benzeri ayırma',
            'membran tuzu geri tutsun',
            'kök benzeri seçici tuz geçişi',
        ],
        "mechanism": 'Bazı mangrovlar su alırken tuzun önemli bölümünün köke girişini sınırlar.',
        "solution": 'Tuz geçişini seçici azaltan katmanlı membran deneyi.',
        "pilot_test": 'Giriş ve çıkış iletkenliğini ve su akısını birlikte ölçün.',
        "source_title": 'Genetic and molecular mechanisms underlying mangrove adaptations to intertidal environments',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC8693430/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Avicennia yaprağının tuz salgılayan bezleri',
        "category": 'Su Arıtma ve Döngüsellik',
        "keywords": [
            'yüzeyde tuzu tek noktada biriktirmek',
            'tuzlu yüzeyde bölgesel kristal toplama',
            'membrandan çıkan tuzu ayrı toplamak',
        ],
        "mechanism": 'Yaprak bezleri tuzu yüzeye salgılayabilir.',
        "solution": 'Tuzun toplanacağı bölgeleri belirleyen seçici dış yüzey.',
        "pilot_test": 'Birikimin konumunu ve alan başına tuz kütlesini ölçün.',
        "source_title": 'Salt secretion in the mangrove Avicennia marina: effects of hypersalinity',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/39916489/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Tuzcul Atriplex’in tuz biriktiren kabarcıkları',
        "category": 'Su Arıtma ve Döngüsellik',
        "keywords": [
            'yüzeyde çözünmüş tuzu ayrı ceplere almak',
            'küçük kesede tuz tutmak',
            'temizlenebilir tuz cebi yüzeyi',
        ],
        "mechanism": 'Atriplex’in epidermal kabarcık hücreleri iyonları depolayabilir.',
        "solution": 'Çıkarılabilir küçük toplama ceplerine sahip iyon tutucu yüzey.',
        "pilot_test": 'Toplanan iyon miktarını ve yüzey yeniden kullanımını ölçün.',
        "source_title": 'Epidermal bladder cells confer salinity stress tolerance in the halophyte quinoa and Atriplex species',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/28558173/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Sphagnum yosununun su depolayan hücreleri',
        "category": 'Su Yönetimi',
        "keywords": [
            'sulama yüzeyi suyu kısa sürede kaybediyor',
            'gözenekli katman su deposu olsun',
            'hafif yüzeyde su tutma hücreleri',
        ],
        "mechanism": 'Sphagnum yosunundaki boş hiyalin hücreler su depolamaya katkı verir.',
        "solution": 'Su depolayan geniş hücrelerden oluşan hafif yüzey katmanı.',
        "pilot_test": 'Eş kütlede emilen suyu ve salım süresini ölçün.',
        "source_title": 'Mechanisms behind species-specific water economy responses to water level drawdown in peat mosses',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC7523593/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Saguaro kaktüsünün genişleyebilen kaburgaları',
        "category": 'Su Yönetimi',
        "keywords": [
            'sıvı tankı dolunca hacmi genişlesin',
            'körüklü hazne dolumda şişiyor',
            'sabit kabuk yerine genişleyen depo',
        ],
        "mechanism": 'Kaburgalı gövde su depolama durumuna göre biçim değiştirebilir.',
        "solution": 'Esnek kaburgalı ve değişken hacimli küçük hazne.',
        "pilot_test": 'Dolum çevrimlerinde hacim değişimini ve gerilimi ölçün.',
        "source_title": 'Plants - Saguaro National Park (U.S. National Park Service)',
        "source_url": 'https://www.nps.gov/sagu/learn/nature/plants.htm',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Mantar meşesi kabuğunun kapalı hücreleri',
        "category": 'Malzeme ve Döngüsellik',
        "keywords": [
            'yalıtım levhası sıkışınca toparlanmıyor',
            'esnek kapalı hücreli izolasyon',
            'az kütlede ısı ve darbe yalıtımı',
        ],
        "mechanism": 'Mantar dokusu hava içeren kapalı hücreli bir yapı oluşturur.',
        "solution": 'Kapalı hücreli hafif yalıtım ve sızdırmazlık numunesi.',
        "pilot_test": 'Isıl direnç ve basma sonrası toparlanmayı ölçün.',
        "source_title": 'The rationale behind cork properties: A review of structure and chemistry',
        "source_url": 'https://bioresources.cnr.ncsu.edu/BioRes_10/BioRes_10_3_Review_Pereira_Rationale_Cork_Prop_Struct_Chem_7095.pdf',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Kenevir gövdesinin dış lif iç öz ayrımı',
        "category": 'Malzeme ve Döngüsellik',
        "keywords": [
            'aynı malzemeden sert dış yumuşak iç panel',
            'lifli gövdede hafif çekirdek',
            'gövde kabuğu ve özü farklı işlensin',
        ],
        "mechanism": 'Gövde dışındaki bast lifleri ile odunsu iç bölge farklı özellik taşır.',
        "solution": 'Lifli dış yüz ve hafif iç çekirdekten biyobazlı panel.',
        "pilot_test": 'Eş yoğunlukta eğilme rijitliğini ve su alımını ölçün.',
        "source_title": 'Phenotypic Variation of Cell Wall Composition and Stem Morphology in Hemp (Cannabis sativa L.): Optimization of Methods',
        "source_url": 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6671528/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Keten gövdesinin selüloz demetleri',
        "category": 'Malzeme ve Döngüsellik',
        "keywords": [
            'bitkisel çekme takviyesi arıyoruz',
            'keten lifli hafif parça',
            'kompozitte cam lif yerine bitkisel lif',
        ],
        "mechanism": 'Keten bast lifleri selülozca zengin demetler halinde yük taşır.',
        "solution": 'Yönlendirilmiş bitkisel lifli kompozit numune.',
        "pilot_test": 'Çekme dayanımı ve nem çevrimi sonrası değişimi ölçün.',
        "source_title": 'Extraction of cellulose fibers from flax and hemp: a review',
        "source_url": 'https://link.springer.com/article/10.1007/s10570-021-04051-x',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Pamuk lifinin şişip bükülen hücre duvarı',
        "category": 'Malzeme ve Üretim',
        "keywords": [
            'ıslanınca bükülen ince şerit',
            'tek lif nemle şekil değiştirsin',
            'kuruyan lifin doğal kıvrılması',
        ],
        "mechanism": 'Pamuk lifinin hücre duvarı yapısı kuruma sırasında kıvrımlı geometriye katkı verir.',
        "solution": 'Nem değişimiyle geometrisi değişen selüloz lif düzeneği.',
        "pilot_test": 'Nem döngüsünde eğrilik ve geri dönüş süresini ölçün.',
        "source_title": 'Cotton Physiology: Cotton fibre development and structure',
        "source_url": 'https://www.cotton.org/foundation/reference-books/cotton-physiology/upload/COTTON-PHYSIOLOGY-Chapter-23.pdf',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Su sümbülünün hava dolu yaprak sapı',
        "category": 'Akışkanlık ve Yüzdürme',
        "keywords": [
            'hafif yüzen sapın içi hava tutmalı',
            'su yüzeyinde gözenekli taşıyıcı',
            'batmayan içi boş biyobazlı destek',
        ],
        "mechanism": 'Bazı su sümbüllerinin şişkin sapındaki hava dokusu yüzdürmeye katkı verir.',
        "solution": 'Hava cepli hafif sap benzeri yüzdürme elemanı.',
        "pilot_test": 'Birim kütlede taşınan yük ve su emilimini ölçün.',
        "source_title": "SS-AGR-380/AG385: Waterhyacinth: Florida's Worst Floating Weed",
        "source_url": 'https://ask.ifas.ufl.edu/publication/AG385',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Kahverengi yosunun gaz kesecikleri',
        "category": 'Akışkanlık ve Yüzdürme',
        "keywords": [
            'suda askıda duran kabloyu yukarı taşımak',
            'ayrık hava keseleri ile yüzdürme',
            'uzun hat boyunca küçük şamandıralar',
        ],
        "mechanism": 'Bazı kahverengi alglerde gaz kesecikleri dokuyu ışığa yakın tutmaya katkı verir.',
        "solution": 'Uzun hat üzerinde dağıtılmış bağımsız yüzdürme keseleri.',
        "pilot_test": 'Derinliğe göre askı yüksekliği ve toplam kaldırmayı ölçün.',
        "source_title": 'BOEM report on kelp and associated marine habitats',
        "source_url": 'https://www.boem.gov/sites/default/files/documents/regions/alaska-ocs-region/BOEM_2021-048.pdf',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Deniz çayırının esnek yaprakları',
        "category": 'Kıyı ve Su Yönetimi',
        "keywords": [
            'esnek sualtı bariyeri akışla eğilsin',
            'dalga gelince yatabilen şerit',
            'akıntıya göre direnci değişen yapay çayır',
        ],
        "mechanism": 'Yapraklar akıntı altında biçim değiştirerek akışla farklı şekilde etkileşir.',
        "solution": 'Esnek şeritlerden dalga kanalı bariyeri prototipi.',
        "pilot_test": 'Farklı akıntı hızlarında şerit eğilmesini ve gerideki dalga yüksekliğini ölçün.',
        "source_title": 'Wave damping by seagrass meadows in combined wave-current conditions',
        "source_url": 'https://aslopubs.onlinelibrary.wiley.com/doi/10.1002/lno.12102',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Tuz bataklığı Spartina’sının gövde yoğunluğu',
        "category": 'Kıyı ve Su Yönetimi',
        "keywords": [
            'sığ kıyıda gövde dizisiyle dalga azaltmak',
            'esnek sap yoğunluğu kıyı koruması',
            'bitki örtüsü ile dalga sönümü ölçmek',
        ],
        "mechanism": 'Bataklık bitki gövdeleri dalga akışıyla etkileşerek enerji kaybına katkı verebilir.',
        "solution": 'Farklı gövde yoğunluğunda deneysel kıyı tamponu.',
        "pilot_test": 'Giriş ve çıkış dalga yüksekliğini yoğunluğa göre karşılaştırın.',
        "source_title": 'Wave Attenuation by Spartina Saltmarshes in the Chesapeake Bay Under Storm Surge Conditions',
        "source_url": 'https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2018JC014865',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Çayır köpeğinin havalandırılan yuvası',
        "category": 'Isı ve Enerji Yönetimi',
        "keywords": [
            'kapalı boşluğa rüzgârla hava verilsin',
            'farklı yükseklikte doğal havalandırma',
            'gömülü haznede pasif hava değişimi',
        ],
        "mechanism": 'Farklı giriş geometrileri dış akışla birlikte yuvada havalandırmayı destekler.',
        "solution": 'Farklı yükseklikte iki açıklığı olan pasif hava kanalı.',
        "pilot_test": 'Rüzgâr hızına göre kanal debisini ve basınç farkını ölçün.',
        "source_title": 'Passive diffusion: Airflow and prairie dog burrow ventilation',
        "source_url": 'https://bpb-ca-c1.wpmucdn.com/sites.uoguelph.ca/dist/c/87/files/2019/11/Okubo-et-al-2002-Passive-Diffusion.pdf',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Çöl tilkisinin büyük kulakla ses yönü bulması',
        "category": 'Sensörler',
        "keywords": [
            'zayıf sesi büyük açıklıkla toplamak',
            'yönlü akustik açıklık tasarımı',
            'zemin altında zayıf ses bulmak',
        ],
        "mechanism": 'Büyük kulak kepçeleri sesi kulak kanalına yönlendirir.',
        "solution": 'Farklı ağız kesitlerinde yönlü akustik toplayıcı.',
        "pilot_test": 'Farklı açılarda sinyal kazancı ve yön hatasını ölçün.',
        "source_title": "Fennec fox | Smithsonian's National Zoo and Conservation Biology Institute",
        "source_url": 'https://nationalzoo.si.edu/animals/fennec-fox',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Balık solungacının karşı akım düzeni',
        "category": 'Isı ve Enerji Yönetimi',
        "keywords": [
            'akış hatları zıt yönde aktarım yapsın',
            'ince kanallarda gaz değişimi',
            'karşı akımla oksijen geçişi',
        ],
        "mechanism": 'Su ile kanın zıt yöndeki akışı solungaç boyunca değişim farkını sürdürür.',
        "solution": 'Karşı akımlı ince kanallı gaz aktarım prototipi.',
        "pilot_test": 'Eş debide paralel ve karşı akım aktarım verimini ölçün.',
        "source_title": '39.1 Systems of Gas Exchange - Biology 2e | OpenStax',
        "source_url": 'https://openstax.org/books/biology-2e/pages/39-1-systems-of-gas-exchange',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Tilapya solungacının çapraz akışla parçacık ayırması',
        "category": 'Su Arıtma ve Döngüsellik',
        "keywords": [
            'ince filtre hızla tıkanıyor',
            'yüzeye paralel akışla ayırmak',
            'filtre üzerindeki parçacık yığılmasını azaltmak',
        ],
        "mechanism": 'Bazı süspansiyonla beslenen balıklarda su filtre yüzeyine paralel bileşenle akarak parçacıkları taşır.',
        "solution": 'Çapraz akışlı küçük filtre prototipi.',
        "pilot_test": 'Eş besleme koşulunda akı, tutma oranı ve tıkanma süresini ölçün.',
        "source_title": 'Crossflow filtration in suspension-feeding fishes',
        "source_url": 'https://www.nature.com/articles/35086574',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Manta vatozunun geri sıçratan filtresi',
        "category": 'Su Arıtma ve Döngüsellik',
        "keywords": [
            'filtre gözenekleri parçacıkla kapanıyor',
            'filtreye değen parçacık geri sekmeli',
            'gözenekten küçük parçacığı ayırmak',
        ],
        "mechanism": 'Manta filtresinde parçacıkların filtre elemanlarından geri sekmesi ayrılmaya katkı verir.',
        "solution": 'Geri sektirici çıkıntıları olan akışlı ayırıcı prototipi.',
        "pilot_test": 'Boyut sınıfına göre ayırma oranını ve basınç kaybını ölçün.',
        "source_title": 'Manta rays feed using ricochet separation, a novel nonclogging filtration mechanism',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/30263959/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Balina köpekbalığının çapraz akışlı filtre pedleri',
        "category": 'Su Arıtma ve Döngüsellik',
        "keywords": [
            'iri parçacık akışta ayrışsın',
            'yüksek debili filtre pedi',
            'geniş yüzeyli su ayırıcısı',
        ],
        "mechanism": 'Balina köpekbalığı filtre pedleriyle sudan besin parçacıklarını ayırır.',
        "solution": 'Geniş yüzeyli ve farklı gözenek dağılımlı ayırıcı ped.',
        "pilot_test": 'Debiye göre parçacık tutma ve basınç kaybını ölçün.',
        "source_title": 'Feeding anatomy, filter-feeding rate, and diet of whale sharks Rhincodon typus during surface ram filter feeding off the Yucatan Peninsula, Mexico',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/20817493/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
    {
        "organism": 'Ay denizanasının kasılma sonrası pasif itişi',
        "category": 'Su Altı Robotik',
        "keywords": [
            'su altı aracında kasılma sonrası süzülmek',
            'aktüatör durduğunda itki devam etsin',
            'vuruşlar arasında itkiyi kullanmak',
        ],
        "mechanism": 'Şemsiye kasılmasından kalan akış yapıları bir sonraki evrede pasif ilerlemeye katkı verir.',
        "solution": 'Aralıklı çalışan şemsiye biçimli itici prototipi.',
        "pilot_test": 'Aynı hareket mesafesinde vuruş aralığına göre enerjiyi ölçün.',
        "source_title": 'Widespread utilization of passive energy recapture in swimming medusae',
        "source_url": 'https://pubmed.ncbi.nlm.nih.gov/29180601/',
        "technical_validation": False,
        "catalogue_expansion": True,
    },
])

for model in model_catalog:
    biological_database.append({
        "organism": model["organism"],
        "category": model["category"],
        "keywords": model["keywords"],
        "mechanism": model["mechanism"],
        "solution": model["solution"],
        "pilot_test": model["pilot_test"],
    })
    scientific_evidence[model["organism"]] = {
        "title": model["source_title"],
        "url": model["source_url"],
        "biological_evidence": True,
        "technical_validation": model["technical_validation"],
        "business_validation": False,
        "catalogue_expansion": model.get("catalogue_expansion", False),
        "note": (
            "Kaynak, modelin biyolojik dayanağıyla ilgilidir. "
            "Karttaki tasarım fikri ve deneme planı NatureOS önerisidir."
        ),
    }

model_categories = {
    "Deniz hıyarının değişken sertlikteki dokusu": "Robotik ve Hassas Kavrama",
    "Erodium tohumunun kendini toprağa yerleştirmesi": "Tarım ve Pasif Mekanizmalar",
    "Hagfish’in suyla temas edince açılan lifleri": "Su Yönetimi ve Sızıntı Kontrolü",
}
model_categories.update({model["organism"]: model["category"] for model in model_catalog})


def show_scientific_evidence(organism, *, heading=True):

    evidence = scientific_evidence.get(organism)

    if evidence is None:
        st.caption(
            "Bu model için bilimsel kaynak "
            "henüz veri tabanına eklenmedi."
        )
        return

    if heading:
        st.markdown("#### Bilimsel Dayanak")

    st.write("**Kaynak:**", evidence["title"])
    if "authors" in evidence:
        st.write("**Yazar ve yıl:**", evidence["authors"], evidence["year"])
        st.write("**Dergi:**", evidence["journal"])

    source_url = evidence.get("url") or f"https://doi.org/{evidence['doi']}"
    st.markdown(f"[Kaynağı aç]({source_url})")

    if evidence.get("catalogue_expansion"):
        st.caption("Biyolojik mekanizma için kaynak bağlantısı eklendi.")
    elif evidence["biological_evidence"]:
        st.success(
            "Biyolojik mekanizma: Doğrulandı"
        )
    else:
        st.info(
            "Biyolojik mekanizma: "
            "Henüz doğrulanmadı"
        )

    if evidence["technical_validation"]:
        st.success(
            "Teknik modelleme: Doğrulandı"
        )
    else:
        st.info(
            "Teknik modelleme: "
            "Henüz doğrulanmadı"
        )

    if evidence["business_validation"]:
        st.success(
            "İşletme uygulaması: Doğrulandı"
        )
    else:
        st.info(
            "İşletme uygulaması: "
            "Henüz doğrulanmadı"
        )

    st.caption(evidence["note"])

problem_categories = {
    "Enerji ve İklim": [
        "enerji",
        "havalandırma",
        "ısı",
        "soğutma",
        "sıcaklık",
        "iklim"
    ],
    "Su ve Kaynaklar": [
        "su",
        "nem",
        "kuraklık",
        "yağmur",
        "arıtma"
    ],
    "Malzeme Teknolojileri": [
        "malzeme",
        "dayanıklılık",
        "hafif",
        "kompozit",
        "lif"
    ],
    "Akış ve Aerodinamik": [
        "sürtünme",
        "direnç",
        "gemi",
        "uçuş",
        "kanat",
        "aerodinamik"
    ],
       "Lojistik ve Tedarik Zinciri Yönetimi": [
        "lojistik",
        "tedarik",
        "rota",
        "dağıtım",
        "ulaşım",
        "optimizasyon"
    ]
}

 


def model_keyword_matches(keyword, words, normalized_problem):
    if " " in keyword:
        return f" {normalize_text(keyword)} " in f" {normalized_problem} "

    keyword_stem = keyword[:-1] + "c" if keyword.endswith("ç") else keyword
    return any(
        word == keyword
        or (len(keyword) >= 4 and word.startswith((keyword, keyword_stem)))
        for word in words
    )


# Each context rule requires one match from both groups.
context_rules = {
    "Tilapya solungacının çapraz akışla parçacık ayırması": (
        ("filtre", "filtrasyon", "süzgeç"),
        ("tıkan", "parçacık birik", "partikül birik", "katı madde birik",
         "debi düş", "debi azal", "debisi düş", "debisi azal", "akış düş", "akış azal", "geçen su miktarı azal"),
    ),
    "Derin deniz cam süngerinin çapraz kafesi": (
        ("ince profil", "hafif taşıyıcı", "raf taşıyıcısı", "kafes", "çerçeve"),
        ("yana yat", "yük altında eğil", "burkul", "yandan eğil"),
    ),
    "Deniz hıyarının değişken sertlikteki dokusu": (
        ("robot kol", "tutucu", "kıskaç", "kavra"),
        ("ez", "kırıl", "çatlat", "düşür"),
    ),
    "Lif kabağının gözenekli iskeleti": (
        ("kargo", "paket", "ambalaj", "sevkiyat"),
        ("darbe", "ezil", "kırıl", "çatla", "çatlı", "birbirine çarp"),
    ),
    "Venüs sinekkapanının temas sayacı": (
        ("sensör", "algılayıcı", "sinyal", "temas"),
        ("yanlış alarm", "yanlış tetik", "gereksiz dur", "parazit"),
    ),
    "Erodium tohumunun kendini toprağa yerleştirmesi": (
        ("tohum", "ekim"),
        ("toprağa gir", "yüzeyde kal", "gömül", "rüzgârla dağıl"),
    ),
    "Hagfish’in suyla temas edince açılan lifleri": (
        ("su", "tank", "depo", "gider"),
        ("sızıntı", "kaçak", "dökül", "sız"),
    ),
    "Halkalı örümcek ağının sesi algılaması": (
        ("makine", "motor", "rulman"),
        ("arıza sesi", "anormal ses", "zayıf titreşim", "uğultu"),
    ),
    "Sahra gümüş karıncasının üçgen tüyleri": (
        ("muhafaza", "sensör", "kutu", "kabin"),
        ("güneşte ısın", "aşırı ısın", "güneş altında", "güneşte çok ısın"),
    ),
    "Çöl yosununun su toplayan kıl uçları": (
        ("sis", "nemli hava", "pus"),
        ("su topla", "damla birik", "su elde et", "su hasadı"),
    ),
    "Buz çiçeğinin suyla açılan kapsülü": (
        ("yağmur", "ıslan", "su gel"),
        ("kapak açıl", "açılan kapak", "kendiliğinden aç"),
    ),
}

# English demonstration cards reuse the evidence records from the Turkish catalogue.
english_demo = {
    "Derin deniz cam süngerinin çapraz kafesi": (
        "Deep-sea glass sponge lattice",
        ("lattice buckling", "lightweight frame buckles", "thin profiles bend sideways", "lattice buckles"),
        "Compare a conventional lattice with a double-diagonal lattice at equal mass. Record the load at buckling.",
    ),
    "Deniz hıyarının değişken sertlikteki dokusu": (
        "Sea cucumber variable-stiffness tissue",
        ("robot gripper crushes", "gripper damages", "fragile parts break", "robot arm crushes"),
        "Compare a fixed-stiffness gripper with a variable-stiffness prototype. Record crushing and drop rates.",
    ),
    "Lif kabağının gözenekli iskeleti": (
        "Loofah fibre network",
        ("products break in shipping", "packaging absorbs impact", "packaging crushes", "shipping damage"),
        "Drop-test the current cushioning and a fibre-network insert of equal mass. Record peak acceleration and permanent deformation.",
    ),
    "Venüs sinekkapanının temas sayacı": (
        "Venus flytrap signal counting",
        ("false alarms", "sensor triggers too easily", "false trigger", "single touch triggers"),
        "Compare single-event and repeated-event triggers using recorded signals. Count false alarms and missed events.",
    ),
    "Erodium tohumunun kendini toprağa yerleştirmesi": (
        "Erodium self-burying seed mechanism",
        ("seeds stay on the surface", "seeds do not enter the soil", "aerial seeding"),
        "Compare bare seeds with seeds in humidity-driven carriers. Measure burial rate and depth under the same conditions.",
    ),
    "Hagfish’in suyla temas edince açılan lifleri": (
        "Hagfish rapidly deploying fibres",
        ("tank is leaking", "tank leak", "water spill", "leak reaches the drain"),
        "Use clean water at bench scale to measure how quickly a fibre barrier deploys and how much water passes through.",
    ),
    "Sahra gümüş karıncasının üçgen tüyleri": (
        "Saharan silver ant triangular hairs",
        ("enclosure overheats in the sun", "outdoor sensor overheats", "passive cooling surface"),
        "Expose two identical enclosures with different surface finishes to the same light and record their internal temperatures.",
    ),
    "Halkalı örümcek ağının sesi algılaması": (
        "Orb-weaving spider acoustic web",
        ("detect machine faults by sound", "machine makes an unusual noise", "weak vibration across a wide area"),
        "Compare a tensioned fibre surface with a point sensor using recorded machine sounds at different noise levels.",
    ),
}


def normalize_text(text):
    text = unicodedata.normalize("NFC", text).replace("İ", "i").casefold()
    text = unicodedata.normalize("NFKD", text.replace("ı", "i"))
    text = "".join(char for char in text if not unicodedata.combining(char))
    return " ".join(re.findall(r"[^\W_]+", text))


def context_terms(organism, normalized):
    groups = context_rules.get(organism, ())
    hits = []
    for group in groups:
        matched = next(
            (term for term in group
             if re.search(r"(?<!\w)" + re.escape(normalize_text(term)) + r"(?:\w*)\b", normalized)),
            None,
        )
        if not matched:
            return []
        hits.append(matched)
    return hits


def analyze_models(problem):
    normalized = normalize_text(problem)
    legacy_words = [word.strip(".,!?;:()") for word in problem.lower().split()]
    grouped = {}
    for item in biological_database:
        organism = item["organism"]
        matched = {}
        for keyword in item["keywords"]:
            if model_keyword_matches(keyword, legacy_words, normalized):
                matched.setdefault(normalize_text(keyword), keyword)
        matched = set(matched.values())
        context = context_terms(organism, normalized)
        if not matched and not context:
            continue

        group = grouped.setdefault(organism, {
            "total_score": 0, "mechanisms": [], "matched_keywords": set(), "context": set(),
        })
        group["matched_keywords"].update(matched)
        group["context"].update(context)
        group["total_score"] += len(matched)
        group["mechanisms"].append(item)

    def rank(entry):
        group = entry[1]
        return (
            any(" " in term for term in group["matched_keywords"]),
            bool(group["context"]),
            group["total_score"],
        )

    return dict(sorted(grouped.items(), key=rank, reverse=True))


def model_reason(group):
    parts = []
    if group["matched_keywords"]:
        parts.append("Eşleşen ifadeler " + ", ".join(sorted(group["matched_keywords"])))
    if group["context"]:
        parts.append("Birlikte görülen problem ipuçları " + ", ".join(sorted(group["context"])))
    return ". ".join(parts)


def csv_bytes(fields, rows):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for row in rows:
        writer.writerow({
            key: "'" + value if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")) else value
            for key, value in row.items()
        })
    return ("\ufeff" + output.getvalue()).encode("utf-8")


def render_discovery():
    st.header("Biyolojik modelleri keşfet")
    query = normalize_text(st.text_input("Model, mekanizma veya işlev ara"))
    categories = sorted(set(model_categories.values()))
    selected = st.selectbox("Uygulama alanı", ["Tümü", *categories, "Kategorisi girilmemiş"])
    by_name = {}
    for item in biological_database:
        organism = item["organism"]
        category = model_categories.get(organism, "Kategorisi girilmemiş")
        if selected not in ("Tümü", category):
            continue
        text = normalize_text(" ".join([organism, category, item["mechanism"], item["solution"], *item["keywords"]]))
        if all(term in text for term in query.split()):
            by_name.setdefault(organism, []).append(item)

    st.caption(f"{len(by_name)} model")
    page_size = 20
    page_count = (len(by_name) + page_size - 1) // page_size
    page = st.selectbox("Katalog sayfası", list(range(1, page_count + 1))) if page_count > 1 else 1
    start = (page - 1) * page_size
    for organism, items in sorted(by_name.items())[start:start + page_size]:
        with st.expander(organism):
            for item in items:
                st.write(item["mechanism"])
                st.write(item["solution"])
                if item.get("pilot_test"):
                    st.write("**İlk deneme**", item["pilot_test"])
            show_scientific_evidence(organism, heading=False)


def render_english_demo(*, examples_only=False):
    st.header("Explore a business problem")
    st.markdown("**Ayşe Meriç Yazıcı**")
    examples = [
        "The lightweight frame buckles.",
        "Our robot gripper crushes fragile parts.",
        "The sensor triggers too easily.",
    ]
    if examples_only:
        problem = st.selectbox("Example", examples)
    else:
        example = st.selectbox("Example", ["Write my own", *examples])
        problem = st.text_area("Describe the problem", value="" if example == "Write my own" else example, key=f"english_{example}")
    if not st.button("Find biological models"):
        return
    normalized = f" {normalize_text(problem)} "
    matches = []
    for organism, (name, phrases, test) in english_demo.items():
        hits = [phrase for phrase in phrases if f" {normalize_text(phrase)} " in normalized]
        if hits:
            matches.append((len(hits), organism, name, hits, test))
    if not matches:
        st.info("No matching model was found in this demo. Try one of the examples above.")
    for _, organism, name, hits, test in sorted(matches, reverse=True):
        with st.expander(name, expanded=True):
            st.write("**Why this model appeared**", ", ".join(hits))
            st.write("**First test**", test)
            evidence = scientific_evidence[organism]
            source = evidence.get("url") or f"https://doi.org/{evidence['doi']}"
            st.markdown(f"[Read the research source]({source})")
            st.caption("Proposed test. Record results from your own operating conditions.")


pilot_cases = {
    "Ambalaj darbe testi": ("Lif kabağının gözenekli iskeleti", "Tepe ivme", "g", False),
    "Hafif kafes burkulma testi": ("Derin deniz cam süngerinin çapraz kafesi", "Burkulma yükü", "N", True),
    "Hassas robot kavrama testi": ("Deniz hıyarının değişken sertlikteki dokusu", "Hasarlı ürün oranı", "%", False),
}


def pilot_change(baseline, candidate, higher_is_better):
    difference = candidate - baseline
    benefit = difference if higher_is_better else -difference
    return difference, benefit / abs(baseline) * 100 if baseline else None


def render_pilot():
    st.header("İşletme pilotu ve ölçüm")
    case = st.selectbox("Pilot senaryosu", ["Kendi denemem", *pilot_cases])
    if case in pilot_cases:
        model, metric, unit, higher = pilot_cases[case]
        st.write(f"**Biyolojik model** {model}")
        item = next(item for item in biological_database if item["organism"] == model)
        st.write("**Deneme planı**", item["pilot_test"])
    else:
        model = st.selectbox("Biyolojik model", sorted({item["organism"] for item in biological_database}))
        metric, unit, higher = "", "", False

    with st.form(f"pilot_{case}"):
        case_id = st.text_input("Vaka kodu", placeholder="Örn. PILOT-001")
        measure = st.text_input("Gösterge", value=metric)
        measure_unit = st.text_input("Ölçü birimi", value=unit)
        baseline = st.number_input("Mevcut tasarımın ölçümü", value=None)
        candidate = st.number_input("Deneme tasarımının ölçümü", value=None)
        direction = st.selectbox("Hedef", ["Daha düşük değer", "Daha yüksek değer"], index=int(higher))
        conditions = st.text_area("Karşılaştırma koşulları, tekrar sayısı ve gözlemler")
        submitted = st.form_submit_button("Sonucu hesapla")
    if submitted:
        if baseline is None or candidate is None or not all(
            value.strip() for value in (case_id, measure, measure_unit)
        ):
            st.warning("Vaka kodunu, göstergeyi, ölçü birimini ve iki ölçümü girin.")
            return
        difference, benefit = pilot_change(baseline, candidate, direction == "Daha yüksek değer")
        row = dict(natureos_surumu=NATUREOS_VERSION, vaka=case_id, model=model, gosterge=measure, birim=measure_unit,
                   mevcut=baseline, deneme=candidate, fark=difference, hedef=direction,
                   hedef_yonunde_degisim_yuzde=benefit, kosullar=conditions)
        st.session_state["pilot_result"] = (case, row)
    saved = st.session_state.get("pilot_result")
    if saved and saved[0] == case:
        row = saved[1]
        st.write(f"**Ölçüm farkı** {row['fark']:+.3g} {row['birim']}")
        benefit = row["hedef_yonunde_degisim_yuzde"]
        st.caption("Başlangıç değeri sıfır olduğunda yüzde değişim hesaplanamaz." if benefit is None else f"Hedef yönünde değişim %{benefit:+.2f}")
        st.download_button("Vaka kaydını CSV olarak indir", csv_bytes(row.keys(), [row]), "natureos_pilot.csv", "text/csv")


def evaluate_cases(rows):
    known_models = {item["organism"] for item in biological_database}
    results = []
    for index, row in enumerate(rows, 1):
        problem = (row.get("problem") or "").strip()
        expected = {(value.strip()) for value in (row.get("expected_models") or "").split("|") if value.strip()}
        if not problem or not expected:
            raise ValueError(f"{index}. vaka için problem ve beklenen model girilmeli.")
        unknown = expected - known_models - {"NO_MATCH"}
        if unknown:
            raise ValueError(f"{index}. vakada tanınmayan model: {', '.join(sorted(unknown))}")
        if "NO_MATCH" in expected and len(expected) > 1:
            raise ValueError(f"{index}. vakada NO_MATCH tek başına kullanılmalı.")

        ranked = list(analyze_models(problem))
        no_match = expected == {"NO_MATCH"}
        results.append({
            "natureos_version": NATUREOS_VERSION,
            "case_id": (row.get("case_id") or str(index)).strip(),
            "problem": problem,
            "expected_models": " | ".join(sorted(expected)),
            "ranked_models": " | ".join(ranked),
            "top_1": (not ranked if no_match else bool(expected.intersection(ranked[:1]))),
            "top_3": (not ranked if no_match else bool(expected.intersection(ranked[:3]))),
            "no_result": not ranked,
            "irrelevant_top_3": sum(model not in expected for model in ranked[:3]),
        })
    return results


def render_evaluation():
    st.header("Makale için eşleştirme değerlendirmesi")
    st.write("Kuralları geliştirmek için kullanılmamış Türkçe problem cümleleri seçin. Uygun modelleri sonuçları görmeden uzman değerlendirmesiyle belirleyin. Birden fazla uygun modeli | ile ayırın. Eşleşme beklenmiyorsa NO_MATCH yazın.")
    with st.expander("Makale için yöntem taslağı"):
        st.markdown(
            "**Amaç.** İşletme problemlerini biyolojik mekanizmalarla eşleştiren "
            "NatureOS prototipinin önerilerini değerlendirmek.\n\n"
            "**Yöntem.** Prototip, sözlükteki problem ifadelerini ve birlikte "
            "görülen problem ipuçlarını eşleştirir. Değerlendirmede kod sürümü, "
            "senaryo seçimi, uzman etiketleme süreci, ilk sıra ve ilk üç isabeti raporlanır. "
            "İşletme denemelerinde ölçüm koşulları ve karşılaştırılan tasarımlar kaydedilir.\n\n"
            "**Yapay zekâ kullanımı.** Python/Streamlit kodu, yazarın belirlediği "
            "işlevsel gereksinimler doğrultusunda OpenAI ChatGPT kullanılarak üretildi ve güncellendi. "
            "Yerel tarayıcı kontrolleri ve araştırma değerlendirmesi yöntem bölümünde belgelenir."
        )
    fields = ("case_id", "problem", "expected_models")
    template = [{"case_id": f"TEST-{index:03d}", "problem": "", "expected_models": ""} for index in range(1, 51)]
    st.download_button("50 vakalık boş şablonu indir", csv_bytes(fields, template), "natureos_degerlendirme.csv", "text/csv")
    names = [{"model": name} for name in sorted({item["organism"] for item in biological_database})]
    st.download_button("Etiketleme için model adlarını indir", csv_bytes(("model",), names), "natureos_model_adlari.csv", "text/csv")
    upload = st.file_uploader("Etiketli CSV dosyası", type=["csv"])
    if upload is None or not st.button("Değerlendirmeyi çalıştır"):
        return
    try:
        data = upload.getvalue().decode("utf-8-sig")
        delimiter = ";" if data.splitlines() and ";" in data.splitlines()[0] else ","
        reader = csv.DictReader(io.StringIO(data), delimiter=delimiter)
        if not set(fields).issubset(reader.fieldnames or []):
            raise ValueError("CSV, case_id, problem ve expected_models sütunlarını içermeli.")
        results = evaluate_cases(reader)
        if not results:
            raise ValueError("CSV en az bir etiketli vaka içermeli.")
    except (ValueError, csv.Error) as error:
        st.error(str(error))
        return
    positive_cases = [row for row in results if row["expected_models"] != "NO_MATCH"]
    negative_cases = [row for row in results if row["expected_models"] == "NO_MATCH"]
    st.write(f"**Toplam vaka sayısı** {len(results)}")
    if positive_cases:
        top_1 = 100 * sum(row["top_1"] for row in positive_cases) / len(positive_cases)
        top_3 = 100 * sum(row["top_3"] for row in positive_cases) / len(positive_cases)
        st.write(f"**Model beklenen vakalar** {len(positive_cases)} · **İlk sırada isabet** %{top_1:.1f} · **İlk üçte isabet** %{top_3:.1f}")
    if negative_cases:
        correctly_unmatched = sum(row["no_result"] for row in negative_cases)
        st.write(f"**Model beklenmeyen vakalar** {len(negative_cases)} · **Doğru biçimde eşleşmesiz** {correctly_unmatched}")
    st.write(f"**Sonuç bulunamayan tüm vakalar** {sum(row['no_result'] for row in results)} · **İlk üçteki ilgisiz öneriler** {sum(row['irrelevant_top_3'] for row in results)}")
    st.dataframe(results, hide_index=True)
    st.download_button("Değerlendirme sonuçlarını indir", csv_bytes(results[0].keys(), results), "natureos_test_sonuclari.csv", "text/csv")


def render_public_demo():
    st.header("Ücretsiz demo")
    examples = {
        "Su arıtma": "İnce filtre hızla tıkanıyor.",
        "Ambalaj": "Cam kavanozlarımız kargoda birbirine çarpıp çatlıyor.",
        "Robotik": "Robot tutucu hassas parçaları eziyor.",
    }
    case = st.selectbox("Örnek problem seçin", list(examples))
    problem = examples[case]
    st.write(problem)
    if st.button("Örneği analiz et"):
        matches = analyze_models(problem)
        if not matches:
            st.info("Bu örnek için eşleşme bulunamadı.")
        for name, group in list(matches.items())[:2]:
            st.subheader(name)
            st.write(model_reason(group))
            for mechanism in group["mechanisms"]:
                st.write(mechanism["solution"])
            show_scientific_evidence(name)


def render_paid_pilot():
    st.header("Ücretli kurumsal pilot")
    st.write(
        "İşletmenizin bir tasarım problemini birlikte ele alalım. "
        "Ayşe Meriç Yazıcı, NatureOS önerilerini değerlendirerek işletmenize özel "
        "bir rapor ve ilk deneme planı hazırlar."
    )
    st.write("Kapsam ve fiyat, görüşme sonrasında teklif olarak paylaşılır.")
    try:
        email = str(st.secrets.get("NATUREOS_PILOT_EMAIL", "")).strip()
    except FileNotFoundError:
        email = ""
    if re.fullmatch(r"[a-zA-Z0-9._+%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", email):
        st.markdown(f"[Pilot için e-posta gönder](mailto:{email}?subject=NatureOS%20kurumsal%20pilot)")
    else:
        st.info("Pilot başvuruları yakında açılacak.")


if os.environ.get("NATUREOS_MODE") != "research":
    page = st.sidebar.radio("NatureOS", ("Ücretsiz demo", "Ücretli kurumsal pilot", "English demo"))
    if page == "Ücretli kurumsal pilot":
        render_paid_pilot()
    elif page == "English demo":
        render_english_demo(examples_only=True)
    else:
        render_public_demo()
    st.stop()


page = st.sidebar.radio(
    "NatureOS", ("Problem analizi", "Model keşfi", "İşletme pilotu", "Makale değerlendirmesi", "English demo")
)
pages = {
    "Model keşfi": render_discovery,
    "İşletme pilotu": render_pilot,
    "Makale değerlendirmesi": render_evaluation,
    "English demo": render_english_demo,
}
if page in pages:
    pages[page]()
    st.stop()


st.header("🔬 Akıllı Problem Analizi")

problem = st.text_area(
    "Çözmek istediğiniz problemi açıklayın:",
    placeholder="Örneğin: Binalarda enerji tüketimini azaltmak istiyorum.",
    height=130
)

if st.button("🔍 Problemi Analiz Et"):

    if not problem.strip():
        st.warning("Lütfen bir problem yazın.")

    else:
        st.subheader("📊 NatureOS Analiz Raporu")

        grouped_results = analyze_models(problem)
        problem_lower = problem.replace("I", "ı").replace("İ", "i").lower()

        
        # Problem kategorilerini belirle
        category_results = []

        for category, keywords in problem_categories.items():
            category_score = 0

            
            for keyword in keywords:
                for word in problem_lower.split():
                    clean_word = word.strip(".,!?;:()")

                    keyword_stem = keyword

                    if keyword.endswith("ç"):
                        keyword_stem = keyword[:-1] + "c"

                    if (
                        clean_word == keyword
                        or (
                            len(keyword) >= 4
                            and (
                                clean_word.startswith(keyword)
                                or clean_word.startswith(keyword_stem)
                            )
                        )
                    ):
                        category_score += 1
                        break


            if category_score > 0:
                category_results.append(
                    (category_score, category)
                )

        existing_categories = {category for _, category in category_results}
        for organism in grouped_results:
            category = model_categories.get(organism)
            if category and category not in existing_categories:
                category_results.append((0, category))
                existing_categories.add(category)

        category_results.sort(reverse=True)

        if category_results:
            st.markdown("### 🧭 Problem Kategorileri")

            for category_score, category in category_results:
                if category_score:
                    st.write(f"**{category}** — {category_score} anahtar kelime eşleşmesi")
                else:
                    st.write(f"**{category}** — problem ifadesi eşleşmesi")
        else:
            st.info(
                "Problem için henüz bir teknoloji "
                "kategorisi belirlenemedi."
            )

        report_lines = [
            "NATUREOS - BIYOMIMETIK ANALIZ RAPORU",
            "=" * 45,
            "",
            f"Problem: {problem}",
            "",
            f"Bulunan biyolojik model sayisi: {len(grouped_results)}",
            ""
        ]

        for organism, group in grouped_results.items():
            report_lines.append(f"BIYOLOJIK MODEL: {organism}")
            report_lines.append("-" * 35)

            
            total_keywords = {
                keyword for item in group["mechanisms"]
                for keyword in item["keywords"]
            }
            matched_keywords = group["matched_keywords"]
            coverage = (
                len(matched_keywords) / len(total_keywords) * 100
                if total_keywords else 0
            )

            report_lines.append(
                f"Eslesen anahtar kelime: "
                f"{len(matched_keywords)} / {len(total_keywords)}"
            )

            report_lines.append(
                f"Anahtar kelime kapsama orani: %{coverage:.0f}"
            )

            report_lines.append(
                model_reason(group)
            )
            report_lines.append("")

            record = scientific_evidence.get(organism)
            if record:
                source_url = record.get("url") or f"https://doi.org/{record['doi']}"
                report_lines.append(f"Bilimsel kaynak: {record['title']} ({source_url})")

            for item in group["mechanisms"]:
                report_lines.append(
                    f"Dogal mekanizma: {item['mechanism']}"
                )
                report_lines.append(
                    f"Teknik cozum: {item['solution']}"
                )
                if "explanation" in item:
                    report_lines.append(f"Açıklama: {item['explanation']}")
                if "pilot_test" in item:
                    report_lines.append(f"İlk deneme: {item['pilot_test']}")
                report_lines.append("")

        report_lines.append(
            "Not: Bu rapor otomatik anahtar kelime "
            "eslestirmesiyle olusturulmustur. "
            "Teknik oneriler bilimsel olarak "
            "dogrulanmalidir."
        )

        st.session_state["last_report"] = "\n".join(report_lines)


        if grouped_results:
            st.success(
                f"{len(grouped_results)} farklı biyolojik model bulundu."
            )

            
            st.subheader("📈 Biyomimetik Eşleşme Değerlendirmesi")

            for organism, group in grouped_results.items():
                total_keywords = {
                    keyword for item in group["mechanisms"]
                    for keyword in item["keywords"]
                }
                matched_keywords = group["matched_keywords"]
                coverage = (
                    len(matched_keywords) / len(total_keywords) * 100
                    if total_keywords else 0
                )

                st.write(f"**{organism}**")
                st.write(
                    f"Eşleşen anahtar kelime: "
                    f"{len(matched_keywords)} / {len(total_keywords)}"
                )
                if group["context"]:
                    st.caption(model_reason(group))
                st.progress(coverage / 100)
                st.caption(
                    f"Anahtar kelime kapsama oranı: %{coverage:.0f}"
                )


            sorted_groups = list(grouped_results.items())

            st.subheader("📊 Biyomimetik Çözüm Karşılaştırma Tablosu")

            comparison_data = []

            
            for organism, group in sorted_groups:
                total_keywords = {
                    keyword for item in group["mechanisms"]
                    for keyword in item["keywords"]
                }
                matched_keywords = group["matched_keywords"]
                coverage = (
                    len(matched_keywords) / len(total_keywords) * 100
                    if total_keywords else 0
                )

                evidence = scientific_evidence.get(organism)
                if evidence is None:
                    business_status = "Kaynak kaydı yok"
                elif evidence["business_validation"]:
                    business_status = "Doğrulandı"
                else:
                    business_status = "Henüz doğrulanmadı"
                if evidence is None:
                    technical_status = "Kaynak kaydı yok"
                elif evidence["technical_validation"]:
                    technical_status = "Doğrulandı"
                else:
                    technical_status = "Henüz doğrulanmadı"
                comparison_data.append({
                    "Biyolojik Model": organism,
                    "Eşleşme Sayısı": group["total_score"],
                    "Mekanizma Sayısı": len(group["mechanisms"]),
                    "Kapsama Oranı": f"%{coverage:.0f}",
                    "Problem İpuçları": ", ".join(sorted(group["context"])) or "—",
                    "Teknik Doğrulama": technical_status,
                    "İşletme Uygulaması": business_status
                 })


            st.dataframe(
                comparison_data,
                use_container_width=True,
                hide_index=True
            )

            
            csv_buffer = io.StringIO()

            writer = csv.DictWriter(
                csv_buffer,
                fieldnames=comparison_data[0].keys(),
                delimiter=";"
            )

            writer.writeheader()
            writer.writerows(comparison_data)

            csv_content = "\ufeff" + csv_buffer.getvalue()

            st.download_button(
                label="📥 Karşılaştırma Tablosunu Excel İçin İndir",
                data=csv_content.encode("utf-8"),
                file_name="NatureOS_Karsilastirma.csv",
                mime="text/csv",
                key="download_comparison"
            )



            for index, (organism, group) in enumerate(
                sorted_groups, 1
            ):
                with st.expander(
                    f"🌿 Biyolojik Model {index}: {organism}",
                    expanded=True
                ):
                    st.write(
                        "**Toplam anahtar kelime eşleşmesi:**",
                        group["total_score"]
                    )

                    st.write(
                        "**Bulunan mekanizma sayısı:**",
                        len(group["mechanisms"])
                    )
                    st.write(
                        "**Bu model neden önerildi?**", model_reason(group)
                    )
                    show_scientific_evidence(organism)
                    for number, item in enumerate(
                        group["mechanisms"], 1
                    ):
                        st.markdown(f"### Çözüm Kartı {number}")

                        st.write(
                            "**Doğal mekanizma:**",
                            item["mechanism"]
                        )

                        st.write(
                            "**Teknik çözüm önerisi:**",
                            item["solution"]
                        )

                        if "explanation" in item:
                            st.write("**Bilimsel açıklama:**", item["explanation"])

                        if "pilot_test" in item:
                            st.write("**İlk deneme ve ölçülecek sonuç**", item["pilot_test"])
                            st.caption("Ölçümlerinizi kaydetmek için İşletme pilotu sayfasını kullanabilirsiniz.")

                        st.divider()


        else:
            st.info(
                "Bu problem için henüz bir biyolojik "
                "eşleşme bulunamadı. Bilgi tabanı "
                "geliştirilmeye devam ediyor."
            )
            st.caption("Parçayı veya süreci ve gözlediğiniz sorunu birlikte yazın. Örnek: İnce profiller yük altında yana yatıyor.")


# NATUREOS - ANALIZ RAPORU INDIRME

if st.session_state.get("last_report"):
    st.subheader("📄 Analiz Raporunu İndir")

    st.download_button(
        label="📥 Raporu Bilgisayarıma İndir",
        data=st.session_state["last_report"],
        file_name="NatureOS_Analiz_Raporu.txt",
        mime="text/plain",
        key="download_report"
    )

st.divider()

st.caption(
    f"NatureOS {NATUREOS_VERSION} | Biomimetic Innovation Prototype"
)

st.divider()

st.subheader("Bilimsel Kanıt ve Kaynak Merkezi")

selected_source = st.selectbox(
    "Kaynağını görmek istediğiniz modeli seçin",
    ["Model seçin", *sorted(scientific_evidence)],
)
if selected_source in scientific_evidence:
    show_scientific_evidence(selected_source, heading=False)
