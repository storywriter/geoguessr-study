"""Bibliography and small manually transcribed statistical facts.

No copied report prose, scans, or publisher-owned maps are redistributed.
"""
from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parents[1]
SOURCES={}
def source(id,title,publisher,year,url,kind,note='',locator=''):
    SOURCES[id]=dict(id=id,title=title,publisher=publisher,data_year=str(year),url=url,kind=kind,note=note,locator=locator,accessed='2026-09-13')

source('PEW2025','How the Global Religious Landscape Changed From 2010 to 2020, Appendix B','Pew Research Center','2010;2020','https://www.pewresearch.org/wp-content/uploads/sites/20/2025/06/PR_2025.06.09_global-religious-change_appendix-b.pdf','宗教人口推計','2025年公表。国・地域201件、人口10万人以上が対象。百分率は丸められている。服装統計ではない。','Appendix B; source_page in extracted CSV')
source('UN_M49','Standard country or area codes for statistical use (M49)','United Nations Statistics Division','2026','https://unstats.un.org/unsd/methodology/m49/','地理区分','アフリカはintermediate region、それ以外はsub-regionを使用。IranはSouthern Asia、RussiaはEastern Europe。')
source('IND_C01','C-01: Population by religious community, India - 2011','Office of the Registrar General & Census Commissioner, India','2011','https://censusindia.gov.in/nada/index.php/catalog/11361','宗教人口国勢調査','全国・州と取得した州の地区表。2011年当時の行政界。新設州の値として読み替えない。','C-01; Total; Persons/Females; Muslim')
source('BPS2010','Penduduk Menurut Wilayah dan Agama yang Dianut, Sensus Penduduk 2010','Badan Pusat Statistik (Indonesia)','2010','https://sensus.bps.go.id/topik/tabular/sp2010/12/91622/1','宗教人口国勢調査','33州当時。イスラム教徒数・全人口・女性数を保存。宗教人口からヒジャブ着用率を計算しない。')
source('LKA2024','Census of Population and Housing 2024, Final Report, Part II','Department of Census and Statistics, Sri Lanka','2024','https://www.statistics.gov.lk/Slider/Census2024_En','宗教人口国勢調査','2012年・2024年対比表から2024年Islam列を転記。','PDF p.96 / printed p.80, Table 9')
source('PEW_DRESS2010','Muslim Americans: No Signs of Growth in Alienation or Support for Extremism','Pew Research Center','2010;2011','https://www.pewresearch.org/wp-content/uploads/sites/4/legacy-pdf/Muslim-American-Report-10-02-12-fix.pdf','頭を覆う頻度の自己申告調査','米国以外の比較は2010年のムスリム女性。質問は頭を覆う頻度であり、ヒジャブ単独の定義ではない。','Q83, printed p.115 / PDF p.125')
source('PEW_IND_DRESS','Religion in India: Religious clothing and personal appearance','Pew Research Center','2019–2020','https://www.pewresearch.org/religion/2021/06/29/religious-clothing-and-personal-appearance/','衣服種別の自己申告調査','ヒジャブ等の語を回答者に定義していない。ムスリム女性の頭を覆う習慣89%とヒジャブ8%は別の指標。地域集計のNorth等はPew独自区分。','Chapter 9; full report printed p.180')
source('ISEAS2022','The Indonesia National Survey Project 2022','ISEAS – Yusof Ishak Institute','2022','https://www.iseas.edu.sg/wp-content/uploads/2023/01/TRS3_23.pdf','ヒジャブ着用の自己申告調査','Muslim women。通常着用61.9%、状況による34.9%、着けない3.3%。2017年と選択肢が違うため単純な増減比較をしない。','Figure 22, printed p.42 / PDF p.55')
source('GALLUP_TUR','Headscarves and Secularism: Voices From Turkish Women','Gallup','2007','https://news.gallup.com/poll/104257/Headscarves-Secularism-Voices-From-Turkish-Women.aspx','頭を覆う服装の自己申告調査','女性一般が分母。ムスリム女性を分母とするPewとは比較条件が違う。2008年公表。')
source('PEW_US2017','U.S. Muslims: Religious beliefs and practices','Pew Research Center','2017','https://www.pewresearch.org/religion/2017/07/26/religious-beliefs-and-practices/','頭を覆う頻度の自己申告調査','米国のムスリム女性。都市ごとの着用率ではない。')
source('ENVIRONICS2016','Survey of Muslims in Canada 2016','Environics Institute','2016','https://www.environicsinstitute.org/docs/default-source/project-documents/survey-of-muslims-in-canada-2016/final-report.pdf','衣服種別の自己申告調査','ムスリム女性のヒジャブ48%。頭の覆い全体53%とは区別。市別の調査ではない。')
source('BAMF2020','Muslimisches Leben in Deutschland 2020','Bundesamt für Migration und Flüchtlinge','2019','https://www.bamf.de/SharedDocs/Anlagen/DE/Forschung/Forschungsberichte/fb38-muslimisches-leben.html','頭を覆う服装の調査','2021年刊。対象出身国に移民背景のあるムスリム女性・少女の約70%が非着用。年齢・標本の範囲を他調査と揃えていない。')
source('INSEE2020','La diversité religieuse en France : transmissions intergénérationnelles et pratiques selon les origines','INSEE / INED','2019–2020','https://www.insee.fr/fr/statistiques/6793308','ベール着用の自己申告調査','TeO2。ムスリム女性18–49歳の26%がベールを着用。パリ・マルセイユ別の数字ではない。')
source('FRA2024','Being Muslim in the EU','European Union Agency for Fundamental Rights','2022','https://fra.europa.eu/en/publication/2024/being-muslim-eu','生活経験の調査','EUの13か国の特定の移民背景集団の調査。欧州の補足候補を検討する背景資料。差別経験の割合を衣服の着用率として使わない。都市の点座標や各市の率はこの資料の測定値ではない。')
source('MYS_DRESS','Hijabistas: An Analysis of the Hijab and Its Influence on Young Malay Muslim Women in Malaysia','Jurnal Pengajian Media Malaysia, Universiti Malaya','2015','https://jpmm.um.edu.my/article/view/5983','服装に関する質的・探索的研究','全国代表の着用率ではない。マレーシアの服装文化の補助資料。')
source('DOSM2020','Key Findings: Population and Housing Census of Malaysia 2020','Department of Statistics Malaysia','2020','https://www.statistics.gov.my/uploads/publications/20221014150434.pdf','宗教人口国勢調査','KelantanのIslam 95.5%。国全体・半島全体に代入しない。')
source('PSA2020','Religious Affiliation in the Philippines (2020 Census of Population and Housing)','Philippine Statistics Authority','2020','https://psa.gov.ph/content/religious-affiliation-philippines-2020-census-population-and-housing','宗教人口国勢調査','BARMM 90.9%は2020年当時の領域・世帯人口。現在のSuluの所属などと区分が一致しない。')
source('ONS2021','Religion, England and Wales: Census 2021','Office for National Statistics','2021','https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/religion/bulletins/religionenglandandwales/census2021','宗教人口国勢調査','例: Tower Hamlets 39.9%、Blackburn with Darwen 35.0%。英国全域や都市全女性の着用率ではない。')
source('ZAF2022','Census 2022 Statistical Release P0301.4','Statistics South Africa','2022','https://census.statssa.gov.za/assets/documents/2022/P03014_Census_2022_Statistical_Release.pdf','宗教人口国勢調査','Western Cape Islam 5.2%は州の全人口を分母とする。','Table 2.10')
source('STATCAN2021','Ethnocultural diversity in Canadian cities','Statistics Canada','2021','https://www.statcan.gc.ca/o1/en/plus/7238-ethnocultural-diversity-canadian-cities','宗教人口国勢調査','Toronto cityの私的世帯人口でMuslim 9.6%。都市圏・女性だけの分母ではない。')
source('ABS2021','Greater Sydney: 2021 Census All persons QuickStats','Australian Bureau of Statistics','2021','https://www.abs.gov.au/census/find-census-data/quickstats/2021/1GSYD','宗教人口国勢調査','Greater SydneyのIslam 6.3%。都市圏全体。メルボルンの根拠には全国表との比較だけを使用。')
source('CENSUS2011_KISHANGANJ','Kishanganj District Religion Census 2011','Census2011.co.in (secondary transcription)','2011','https://www.census2011.co.in/data/religion/district/62-kishanganj.html','国勢調査の二次転載','67.98%は地区、都市42.62%とは異なる。元統計は2011年。ページ見出しの現在年を統計年にしない。')
source('KOZHIKODE','History of Kozhikode','District Administration, Kozhikode','2026','https://kozhikode.nic.in/en/about-district/history/','地名の確認','Kozhikode = Calicut（カリカット）。Calcutta = Kolkataとは別。統計ではない。')
source('SRINAGAR','Demography','District Administration, Srinagar','2011','https://srinagar.nic.in/demography/','宗教人口の概要','市と地区を区別する。本版の数値はC-01地区表を優先。')
source('SOM_DRESS','Harsh War, Harsh Peace: Abuses by al-Shabaab, the Transitional Federal Government, and AMISOM in Somalia','Human Rights Watch','2009–2010','https://www.hrw.org/reports/2010/04/13/harsh-war-harsh-peace','服装に関する現地聞き取り','南部・中部の服装強制などの記録。全国の着用率調査ではない。ソマリランドまで同じ政治状況を適用しない。')
source('PEW_ATTIRE','Restrictions on women’s religious attire','Pew Research Center','2012–2013','https://www.pewresearch.org/religion/2016/04/05/restrictions-on-womens-religious-attire/','服装の制度・社会状況','チェチェンの公的建物での服装要件を含む。北コーカサス全女性の率ではない。')
for code,name in [('IRN','iran'),('AFG','afghanistan'),('MDV','maldives'),('SAU','saudi-arabia')]:
    source('FCDO-'+code,'Foreign travel advice: '+name+', safety and security','UK Foreign, Commonwealth & Development Office','2026','https://www.gov.uk/foreign-travel-advice/'+name+'/safety-and-security','現行の服装・旅行案内','制度・生活上の案内。街頭着用率の測定ではない。閲覧日時点の情報で、撮影年へ遡及適用しない。')
source('NATURAL_EARTH','1:10m Admin 0 Countries / Admin 1 States and Provinces','Natural Earth','2026','https://www.naturalearthdata.com/about/terms-of-use/','白地図・境界データ','パブリックドメイン。Git commitを固定し、0.012度で簡略化。境界は地理表示用で政治的立場を意味しない。')
source('NOTO','Noto Sans JP','Noto CJK project / Google','2026','https://github.com/notofonts/noto-cjk/tree/f8d157532fbfaeda587e826d4cd5b21a49186f7c/Sans','描画フォント','SIL Open Font License 1.1。キャッシュ内でウェイト400のTrueTypeを生成し、システムフォントと衝突しない固有名を付けてPDFへ埋め込む。')

def add_irf():
    from collect_irf import SLUGS
    discovery=json.loads((ROOT/'data/irf_source_metadata.json').read_text())
    aliases={'CIV':'cote-divoire','RUS':'russia','PSE':'west-bank-and-gaza','MMR':'burma'}
    for code,slug in SLUGS.items():
        source('IRF-'+code,'2023 Report on International Religious Freedom: '+slug,'U.S. Department of State','2023','https://2021-2025.state.gov/reports/2023-report-on-international-religious-freedom/'+aliases.get(code,slug)+'/','宗教の地域分布・社会状況','主にSection I。服装の実測率ではない。報告書中の宗教人口の引用年は別途確認する。')
        d=discovery.get(code,{})
        if d.get('mirror_url'):SOURCES['IRF-'+code]['mirror_url']=d['mirror_url']
        if d.get('original_url'):SOURCES['IRF-'+code]['url']=d['original_url']
        SOURCES['IRF-'+code]['retrieval_status']=d.get('status','original_or_index_only')

def write_sources():
    add_irf()
    (ROOT/'data/sources.json').write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2)+'\n')
    lines=['# 出典一覧','', '統計は服装そのものを測る資料と宗教人口を測る資料に分けて利用する。解説は編集者による要約。報告書全文・原図は転載していない。','']
    for s in SOURCES.values():
        lines += [f'## {s["id"]}', '',f'[{s["title"]}]({s["url"]}) — {s["publisher"]}', '',f'- データ年・参照時点: {s["data_year"]} / 種類: {s["kind"]}',f'- 用途・制限: {s["note"]}']
        if s.get('locator'):lines += ['- 該当箇所: '+s['locator']]
        if s.get('mirror_url'):lines += [f'- [ACCORDによる原報告の保存版]({s["mirror_url"]})']
        elif s.get('retrieval_status') not in [None,'retrieved']:lines += ['- 取得状況: 原報告の参照リンク。本文の地域記述を今回の抽出処理で確認できていないため、服装の直接的根拠には用いない。']
        lines+=['']
    (ROOT/'docs').mkdir(exist_ok=True)
    (ROOT/'docs/SOURCES.md').write_text('\n'.join(lines).rstrip()+'\n')

def write_small_tables():
    facts=[
      ['Zanzibar','TZA',2023,99,'地域人口','推計、概数','IRF-TZA'],
      ['Kelantan','MYS',2020,95.5,'州人口','国勢調査','DOSM2020'],
      ['BARMM2020','PHL',2020,90.9,'2020年当時のBARMM世帯人口','現在の行政区分と異なる','PSA2020'],
      ['Western Cape','ZAF',2022,5.2,'州人口','ケープタウン市の値ではない','ZAF2022'],
      ['Toronto city','CAN',2021,9.6,'市の私的世帯人口','都市圏の値ではない','STATCAN2021'],
      ['Greater Sydney','AUS',2021,6.3,'都市圏人口','地区・女性の値ではない','ABS2021'],
      ['Tower Hamlets','GBR',2021,39.9,'local authorityの全住民','ロンドン市全体の値ではない','ONS2021'],
      ['Blackburn with Darwen','GBR',2021,35.0,'local authorityの全住民','ブラックバーン中心部だけの値ではない','ONS2021'],
      ['Kishanganj district','IND',2011,67.98,'地区人口','国勢調査の二次転載','CENSUS2011_KISHANGANJ'],
    ]
    with (ROOT/'data/manual_statistics.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['area','iso3','year','muslim_percent','denominator_ja','note_ja','source_id']);w.writerows(facts)
    rows=[]
    def dress(iso,area,year,metric,pct,denom,source,note=''):
        rows.append([iso,area,year,metric,pct,denom,source,note])
    for iso,a,b,c,d in [('EGY',62,21,6,12),('IDN',11,18,53,18),('JOR',59,24,10,7),('LBN',58,5,5,31),('NGA',53,16,12,15),('PAK',32,29,10,29),('TUR',56,6,7,28)]:
        for metric,pct in [('head_cover_always',a),('head_cover_most',b),('head_cover_sometimes',c),('head_cover_never',d)]:
            dress(iso,'national',2010,metric,pct,'ムスリム女性','PEW_DRESS2010','頭布全般の頻度。回答丸め・無回答があり合計は100に限らない。')
    for area,head,hijab,niqab,burqa in [('national',89,8,12,64),('North',85,7,15,61),('East',92,7,17,59),('West',90,4,15,67),('South',83,23,1,59),('Northeast',85,7,3,55)]:
        for metric,pct in [('head_cover_practice',head),('hijab',hijab),('niqab',niqab),('burqa',burqa)]:
            dress('IND',area,'2019–2020',metric,pct,'ムスリム女性','PEW_IND_DRESS','Pew独自地域区分。服装用語を調査時に定義していない。Centralは標本不足。')
    for metric,pct in [('hijab_usually',61.9),('hijab_situational',34.9),('hijab_never',3.3)]:dress('IDN','national',2022,metric,pct,'ムスリム女性','ISEAS2022','Figure 22。2017年と選択肢が異なる。')
    dress('USA','national',2017,'head_cover_always',38,'ムスリム女性','PEW_US2017')
    dress('USA','national',2017,'head_cover_most',5,'ムスリム女性','PEW_US2017')
    dress('CAN','national',2016,'hijab',48,'ムスリム女性','ENVIRONICS2016')
    dress('CAN','national',2016,'any_head_cover',53,'ムスリム女性','ENVIRONICS2016')
    dress('FRA','national','2019–2020','veil',26,'ムスリム女性18–49歳（TeO2対象者）','INSEE2020')
    dress('DEU','survey_origins',2019,'no_headscarf',70,'対象出身国に移民背景のあるムスリム女性・少女','BAMF2020','概数。分母・年齢が他調査と異なる。')
    with (ROOT/'data/clothing_surveys.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['iso3','survey_area','year','metric','percent','denominator_ja','source_id','note_ja']);w.writerows(rows)

if __name__=='__main__':write_sources();write_small_tables()
