"""Vector atlas with large, font-checked glyphs and explicit map-to-card links."""
from pathlib import Path
import json,math,os,sys,textwrap,warnings
TOPIC=Path(__file__).resolve().parents[1];ROOT=TOPIC.parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_pdf import PdfPages
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from shapely.geometry import shape,box
from pyproj import Transformer
from shapely.ops import transform
sys.path.insert(0,str(ROOT/'scripts'))
from render_maps import patch,setup as setup_jp
sys.path.pop(0)
from languages import LANGUAGES

DATA=TOPIC/'data';OUT=TOPIC/'output';CACHE=ROOT/'.cache/european-letterforms'
INK='#152f42';MUTED='#566a77';BG='#f4f7fa'
PALETTE=['#b4dcd5','#f4d0b2','#c9c9ed','#bcd4ee','#e8c1d5','#d6dfa9','#e1d2b7']
FONT_NAMES={};FONT_CMAPS={};LOCATIONS=[];TEXT_BOXES=[]

def setup():
    setup_jp()
    for family in ['NotoSans','NotoSansArmenian','NotoSansGeorgian']:
        source=CACHE/(family+'.ttf');dest=CACHE/(family+'-Study.ttf')
        unique='GeoStudy '+family
        if not dest.exists():
            ft=TTFont(source);axes={a.axisTag:(400 if a.axisTag=='wght' else a.defaultValue) for a in ft['fvar'].axes}
            ft=instantiateVariableFont(ft,axes,inplace=False)
            replacements={1:unique,2:'Regular',4:unique+' Regular',6:family+'Study-Regular',16:unique,17:'Regular'}
            for n in ft['name'].names:
                if n.nameID in replacements:n.string=replacements[n.nameID].encode(n.getEncoding())
            ft.recalcTimestamp=False;ft.save(dest)
        fm.fontManager.addfont(str(dest));FONT_NAMES[family]=unique;FONT_CMAPS[family]=TTFont(dest).getBestCmap()
    plt.rcParams.update({'font.family':['GeoGuessr Study JP',*FONT_NAMES.values()],'font.size':11,'svg.fonttype':'path','pdf.fonttype':42,'svg.hashsalt':'european-letterforms-v1'})
    for l in LANGUAGES.values():
        family={'Armenian':'NotoSansArmenian','Georgian':'NotoSansGeorgian'}.get(l['script'],'NotoSans')
        missing=[c for c in l['glyphs']+' '+l['words'] if not c.isspace() and ord(c) not in FONT_CMAPS[family]]
        if missing:raise ValueError(f'Missing glyphs: {l["id"]} {missing}')
    warnings.filterwarnings('error',message='Glyph .* missing from font')

def txt(fig,x,y,s,size=11,color=INK,**kwargs):
    t=fig.text(x,y,s,fontsize=size,color=color,**kwargs);TEXT_BOXES.append(t);return t
def glyph(fig,x,y,s,script,size=22,**kw):
    family=FONT_NAMES[{'Armenian':'NotoSansArmenian','Georgian':'NotoSansGeorgian'}.get(script,'NotoSans')]
    return txt(fig,x,y,s,size,fontfamily=family,**kw)
def footer(fig,page):
    txt(fig,.035,.047,'色は参照する地域、点は代表地点。言語の排他的な境界・人口割合・看板の出現率ではありません。',9,color=MUTED)
    txt(fig,.035,.025,'Natural Earth（public domain）｜出典・資料年・統計の分母：CSV / docs/SOURCES.md｜2026-09-13',8.5,color=MUTED)
    txt(fig,.965,.027,str(page).zfill(2),11,ha='right',color=MUTED)

def background(ax,world,extent,projection=None):
    window=box(*extent)
    for f in world:
        g=shape(f['geometry'])
        if not g.intersects(window):continue
        g=g.intersection(window)
        if projection:g=transform(projection,g)
        patch(ax,g,'#fff',edge='#acb9c1',width=.5)

def savepage(fig,pdf,number,svg=False):
    fig.canvas.draw();renderer=fig.canvas.get_renderer()
    for t in TEXT_BOXES:
        bb=t.get_window_extent(renderer)
        if bb.x0 < -1 or bb.y0 < -1 or bb.x1 > fig.bbox.width+1 or bb.y1 > fig.bbox.height+1:
            raise ValueError('Text outside page: '+t.get_text())
    pdf.savefig(fig)
    fig.savefig(OUT/f'atlas_{number:02d}.png',dpi=140,facecolor='white')
    if svg:
        path=OUT/f'atlas_{number:02d}.svg';fig.savefig(path,metadata={'Date':None},facecolor='white')
        path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
    TEXT_BOXES.clear();plt.close(fig)

def cover(world,countries,pages):
    fig=plt.figure(figsize=(16,11.3),facecolor='white')
    txt(fig,.04,.95,'ヨーロッパ周辺の特徴的な文字形',29,weight='bold')
    txt(fig,.04,.906,'GeoGuessr攻略 02  ｜  国の基本表示と、地域の併記言語を地図で覚える',13,color=MUTED)
    ax=fig.add_axes([.04,.40,.60,.445],facecolor=BG)
    proj=Transformer.from_crs('EPSG:4326','+proj=robin +lon_0=0 +datum=WGS84 +units=m',always_xy=True).transform
    background(ax,world,(-180,-60,180,85),proj)
    for f in countries:patch(ax,transform(proj,shape(f['geometry'])),'#96c9c1',edge='#66988e',width=.35,z=3)
    ax.set_xlim(-17500000,17500000);ax.set_ylim(-6400000,8700000)
    ax.set_aspect('equal');ax.axis('off')
    txt(fig,.065,.40,'対象：国連のヨーロッパ区分＋アルメニア・アゼルバイジャン・ジョージア・キプロス。ロシアは全域。',9,color=MUTED)
    samples=[('Latin','ラテン文字','ã  õ  ø  ł  ř  ő  ə'),('Cyrillic','キリル文字','ы  э  ї  є  ў  ћ  ӕ'),('Greek','ギリシャ文字','Θ  Λ  Ξ  Ω'),('Armenian','アルメニア文字','ա  ե  մ  և'),('Georgian','ジョージア文字','ა  ბ  გ  მ')]
    y=.81
    for script,label,chars in samples:
        txt(fig,.685,y,label,12);glyph(fig,.685,y-.036,chars,script,25);y-=.086
    txt(fig,.05,.338,'使い方',18,weight='bold')
    instructions=['1  まず文字体系を見て、次ページの似た文字の組を比べる。','2  拡大図の番号と右側のカードを対応させ、国の中の位置を覚える。','3  一文字で国を断定せず、短い語・併記・道路や景観と組み合わせる。']
    for i,s in enumerate(instructions):txt(fig,.05,.29-i*.043,s,12)
    txt(fig,.05,.134,'法定の言語でも、看板での使用は少ないことがあります。詳しい公的地位・地域差・根拠はCSVに収録しています。',10,color=MUTED)
    footer(fig,1);return fig

def comparisons():
    fig=plt.figure(figsize=(16,11.3),facecolor='white')
    txt(fig,.04,.95,'まず覚える、似た文字の違い',27,weight='bold')
    txt(fig,.04,.913,'このページは候補を絞る早見表。固有名詞・引用・観光案内・古い綴りには例外があります。',12,color=MUTED)
    items=[
      ('北欧の母音','æ ø å  /  ä ö å','デンマーク・ノルウェー ／ スウェーデン','Latin'),
      ('北大西洋の島','þ ð ö  /  ð ø','アイスランド ／ フェロー諸島','Latin'),
      ('フィンランドの隣','ä ö  /  õ ä ö ü','フィンランド語 ／ エストニア語','Latin'),
      ('バルト海東岸','ā ē ģ ķ  /  ė ą ę ų','ラトビア語 ／ リトアニア語','Latin'),
      ('西スラヴ諸語','ł ą ę  /  ř ů  /  ľ ô','ポーランド語 ／ チェコ語 ／ スロバキア語','Latin'),
      ('中欧の特徴字','ő ű  /  ă ș ț','ハンガリー語 ／ ルーマニア語','Latin'),
      ('イベリア半島','ñ calle  /  ã õ rua','スペイン語 ／ ポルトガル語','Latin'),
      ('スペイン周辺の地域言語','l·l ny  /  tx tz eta','カタルーニャ語 ／ バスク語','Latin'),
      ('ドイツ語圏','ß Straße  /  ss Strasse','ドイツ・オーストリア ／ スイスなど','Latin'),
      ('東スラヴ諸語','ы э  /  ї є ґ  /  ў','ロシア語 ／ ウクライナ語 ／ ベラルーシ語','Cyrillic'),
      ('バルカンのキリル文字','ћ ђ  /  ќ ѓ ѕ','セルビア語 ／ マケドニア語','Cyrillic'),
      ('西アジアのラテン文字','ı İ ğ ş  /  ə','トルコ語・アゼルバイジャン語 ／ 後者の補助','Latin')]
    for i,(title,chars,caption,script) in enumerate(items):
        col=i%3;row=i//3;x=.04+col*.32;y=.855-row*.184
        fig.add_artist(Rectangle((x,y-.15),.30,.163,transform=fig.transFigure,facecolor=BG,edgecolor='none'))
        txt(fig,x+.012,y-.018,title,12,weight='bold');glyph(fig,x+.012,y-.066,chars,script,22)
        for j,line in enumerate(textwrap.wrap(caption,25)):txt(fig,x+.012,y-.107-j*.021,line,10,color=MUTED)
    footer(fig,2);return fig

def regional(page,world,regions,features,occurrences,countries):
    fig=plt.figure(figsize=(16,11.3),facecolor='white');extent=page['extent']
    txt(fig,.035,.95,f'{page["number"]:02d}  {page["title"]}',25,weight='bold')
    txt(fig,.035,.911,'地図の番号 → 日本語の言語名 → 文字形・短い語',12,color=MUTED)
    if page['group'].startswith('ロシア・'):
        txt(fig,.035,.880,'ロシア語が基本。地域公用語の使用地点は限られ、同じ地域の全看板には現れません。',10,color=MUTED)
    elif page['group']=='スイス':
        txt(fig,.035,.880,'色は主な位置を州でまとめた概略です。州内の言語地区は、さらに細かく入り組んでいます。',10,color=MUTED)
    ax=fig.add_axes([.035,.165,.55,.69],facecolor=BG)
    background(ax,world,extent)
    selected=page['region_ids'];colors={rid:PALETTE[i%len(PALETTE)] for i,rid in enumerate(selected)}
    window=box(*extent)
    for rid in sorted(selected,key=lambda rid:regions[rid]['kind']!='national'):
        f=features[rid];g=shape(f['geometry']).intersection(window)
        if g.is_empty:raise ValueError(f'Invisible region {rid} in {page["title"]}')
        if g.geom_type=='Point':ax.scatter(g.x,g.y,s=40,facecolor=colors[rid],edgecolor=INK,zorder=6)
        else:patch(ax,g,colors[rid],edge='#879692',width=.55,z=3,gid=rid)
    ax.set_xlim(extent[0],extent[2]);ax.set_ylim(extent[1],extent[3]);ax.set_aspect(1/max(.3,math.cos(math.radians((extent[1]+extent[3])/2))))
    ax.tick_params(labelsize=8,colors=MUTED);ax.grid(lw=.4,alpha=.2)
    for sp in ax.spines.values():sp.set_color('#d1dce2')
    fig.canvas.draw();used=[]
    # Markers displaced only in screen space; leader lines preserve the anchors.
    for rid in selected:
        g=shape(features[rid]['geometry']).intersection(window);p=g if g.geom_type=='Point' else g.representative_point()
        sx,sy=ax.transData.transform((p.x,p.y))
        choices=[(0,0)]+[(dx,dy) for d in (18,32,50,70,95,120) for dx,dy in ((d,0),(-d,0),(0,d),(0,-d),(d,d),(-d,d),(d,-d),(-d,-d))]
        found=None
        for dx,dy in choices:
            px,py=sx+dx,sy+dy
            if not (ax.bbox.x0+14<px<ax.bbox.x1-14 and ax.bbox.y0+10<py<ax.bbox.y1-10):continue
            if all(abs(px-ux)>29 or abs(py-uy)>21 for ux,uy in used):found=(px,py);break
        if found is None:raise ValueError('No marker position '+rid)
        used.append(found);dest=ax.transData.inverted().transform(found)
        ax.annotate(str(regions[rid]['number']),xy=(p.x,p.y),xytext=dest,fontsize=10,ha='center',va='center',zorder=10,bbox=dict(boxstyle='round,pad=.28',fc='white',ec='#546c78',lw=.6),arrowprops=dict(arrowstyle='-',color='#435c69',lw=.8))
        LOCATIONS.append(dict(page=page['number'],region_id=rid,anchor_lonlat=[p.x,p.y],label_lonlat=list(dest),label_pdf_xy=[found[0]*72/fig.dpi,found[1]*72/fig.dpi],pdf_coordinate_origin='bottom-left',page_size_pt=[1152,813.6],axes_extent_lonlat=extent))
    txt(fig,.045,.119,'塗色は位置の目安です。複数言語の範囲は重なります。周辺の白地は「その言語がない」ことを意味しません。',8.5,color=MUTED)
    x=.613;top=.857;step=.099
    for i,oid in enumerate(page['occurrence_ids']):
        o=occurrences[oid];r=regions[o['region_id']];l=LANGUAGES[o['language_id']];y=top-i*step
        fig.add_artist(Rectangle((x-.011,y-.080),.354,.092,transform=fig.transFigure,facecolor='#f7f9fa',edgecolor='none'))
        fig.add_artist(Rectangle((x-.011,y-.080),.005,.092,transform=fig.transFigure,facecolor=colors[r['id']],edgecolor='none'))
        label=f'{r["number"]:03d}  {r["country_ja"]}｜{r["area_ja"]}'
        lines=textwrap.wrap(label,39)
        txt(fig,x,y,lines[0],9,color=MUTED)
        if len(lines)>1:txt(fig,x,y-.014,lines[1],8.5,color=MUTED)
        langname=l['name_ja'].replace('（バレンシア語を含む）','・バレンシア語')
        txt(fig,x,y-.030,langname,11.2,weight='bold')
        glyph(fig,x,y-.059,l['glyphs'],l['script'],21)
        if l['words']:glyph(fig,x+.171,y-.060,l['words'],l['script'],11,color=MUTED)
    footer(fig,page['number']);return fig

def main():
    setup();OUT.mkdir(exist_ok=True)
    world=json.loads((ROOT/'data/basemap_countries.geojson').read_text())['features']
    countries=json.loads((DATA/'country_shapes.geojson').read_text())['features']
    regions={r['id']:r for r in json.loads((DATA/'regions.json').read_text())}
    features={r['id']:r for r in json.loads((DATA/'study_regions.geojson').read_text())['features']}
    occurrences={o['id']:o for o in json.loads((DATA/'occurrences.json').read_text())}
    pages=json.loads((DATA/'page_definitions.json').read_text())
    output=OUT/'ヨーロッパ周辺の特徴的な文字形_地図帳.pdf'
    with PdfPages(output,metadata={'Title':'ヨーロッパ周辺の特徴的な文字形 / GeoGuessr攻略 02','Author':'GeoGuessr攻略','CreationDate':None,'ModDate':None}) as pdf:
        savepage(cover(world,countries,pages),pdf,1,svg=True);savepage(comparisons(),pdf,2,svg=True)
        for p in pages:
            savepage(regional(p,world,regions,features,occurrences,countries),pdf,p['number'])
            print(f'Page {p["number"]}: {p["title"]}',flush=True)
    (DATA/'map_label_coordinates.json').write_text(json.dumps(LOCATIONS,ensure_ascii=False,indent=2)+'\n')
    # Add useful PDF outline entries without rasterising or changing page content.
    from pypdf import PdfReader,PdfWriter
    writer=PdfWriter();writer.append(PdfReader(output));writer.add_outline_item('対象範囲と使い方',0);writer.add_outline_item('似た文字の早見表',1)
    for p in pages:writer.add_outline_item(p['title'],p['number']-1)
    writer.add_metadata({'/Title':'ヨーロッパ周辺の特徴的な文字形','/Author':'GeoGuessr攻略'})
    with output.open('wb') as f:writer.write(f)
    print(f'Rendered {len(pages)+2} pages; all glyphs present; {len(LOCATIONS)} mapped label coordinates.')

if __name__=='__main__':main()
