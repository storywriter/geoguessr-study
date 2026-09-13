"""Deterministic, shareable cartography; no third-party tiles or image editing AI."""
from pathlib import Path
import json,math,textwrap,os
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME',str(ROOT/'.cache'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import PathPatch,Patch
from matplotlib.path import Path as MPath
from matplotlib.backends.backend_pdf import PdfPages
from pyproj import Transformer
from shapely.geometry import shape,box
from shapely.ops import transform
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data';OUT=ROOT/'output'
COLORS={'高い':'#b82338','やや高い':'#f3b6bd'}
FONT=ROOT/'.cache/NotoSansJP-Regular.ttf'
NUMBERS={}

def setup():
    from fontTools.ttLib import TTFont
    unique_family='GeoGuessr Study JP'
    if not FONT.exists() or TTFont(FONT)['name'].getDebugName(1)!=unique_family:
        vf=ROOT/'.cache/NotoSansJP-VF.ttf'
        if not vf.exists():raise FileNotFoundError('Run python scripts/fetch_assets.py to download the OFL font.')
        from fontTools.varLib.instancer import instantiateVariableFont
        font=instantiateVariableFont(TTFont(vf),{'wght':400},inplace=False)
        # Avoid selecting an installed OTF with the same family name, which
        # matplotlib would embed as Type42 despite its CFF outlines.
        new_names={1:unique_family,2:'Regular',4:unique_family+' Regular',6:'GeoGuessrStudyJP-Regular',16:unique_family,17:'Regular'}
        for entry in font['name'].names:
            if entry.nameID in new_names:entry.string=new_names[entry.nameID].encode(entry.getEncoding())
        font.recalcTimestamp=False
        font.save(FONT)
    fm.fontManager.addfont(str(FONT))
    plt.rcParams.update({'font.family':fm.FontProperties(fname=FONT).get_name(),'font.size':10,'axes.unicode_minus':False,'svg.fonttype':'none','svg.hashsalt':'geoguessr-study-v1','pdf.fonttype':42})

def polygons(g):
    if g.is_empty:return
    if g.geom_type=='Polygon':yield g
    elif g.geom_type in ['MultiPolygon','GeometryCollection']:
        for v in g.geoms:yield from polygons(v)

def patch(ax,g,face,edge='#798188',width=.3,z=1,gid=None):
    for n,p in enumerate(polygons(g)):
        vertices=[];codes=[]
        for ring in [p.exterior,*p.interiors]:
            c=np.array(ring.coords);vertices.extend(c);codes.extend([MPath.MOVETO]+[MPath.LINETO]*(len(c)-2)+[MPath.CLOSEPOLY])
        q=PathPatch(MPath(vertices,codes),facecolor=face,edgecolor=edge,lw=width,zorder=z)
        if gid:q.set_gid(gid+f'-{n}')
        ax.add_patch(q)

def legend(fig,y=.90):
    handles=[Patch(facecolor='white',edgecolor='#8a939b',label='色なし：低い、または判断材料不足'),Patch(facecolor=COLORS['やや高い'],label='薄い赤：日常的に見られる可能性'),Patch(facecolor=COLORS['高い'],label='濃い赤：多く着用すると推定')]
    fig.legend(handles=handles,loc='upper left',bbox_to_anchor=(.04,y),ncol=3,frameon=False,fontsize=10,handlelength=1.8,columnspacing=2)

def footer(fig):
    fig.text(.04,.034,'住民の生活圏についての定性推定。街頭での実測率・GeoGuessrの出題確率ではありません。点は都市内の一部の位置を示します。',fontsize=9,color='#4b5965')
    fig.text(.04,.015,'境界：Natural Earth (public domain)  |  資料：Pew / 各国統計局ほか、2000年以降  |  出典・年・根拠：CSVと docs/SOURCES.md  |  作成 2026-09-13',fontsize=8,color='#697783')

def basemap(ax,world,projection=None,extent=None):
    for f in world:
        g=shape(f['geometry'])
        if extent:g=g.intersection(box(*extent))
        if projection:g=transform(projection,g)
        patch(ax,g,'white',width=.35)

def map_features(ax,features,projection=None,extent=None,annotate=False):
    for f in features:
        g=shape(f['geometry']);p=f['properties'];original=g
        if extent and not g.intersects(box(*extent)):continue
        if extent and g.geom_type!='Point':g=g.intersection(box(*extent))
        if projection:g=transform(projection,g)
        if g.geom_type=='Point':
            ax.scatter(g.x,g.y,s=24,c=COLORS[p['level']],edgecolor='#882033',linewidth=.6,zorder=5)
        else:patch(ax,g,COLORS[p['level']],edge='#a95b66',width=.25,z=3,gid=p['id'])

def world_map(world,features):
    fig=plt.figure(figsize=(16,10),facecolor='#fff')
    fig.text(.04,.958,'ヒジャブの出現率',fontsize=25,weight='bold',color='#172d3d')
    fig.text(.04,.923,'GeoGuessr攻略  /  世界の候補を覚える学習地図',fontsize=12,color='#62737f')
    legend(fig,.90)
    ax=fig.add_axes([.035,.115,.93,.715],facecolor='#f3f7fa')
    proj=Transformer.from_crs('EPSG:4326','+proj=robin +lon_0=0 +datum=WGS84 +units=m',always_xy=True).transform
    basemap(ax,world,projection=proj);map_features(ax,features,projection=proj)
    labels=[('インドネシア',116,-7),('マレーシア',106,7),('インド',78,24),('パキスタン',67,29),('ナイジェリア',6,17),('エジプト',30,27),('ソマリア',50,4),('イラン',56,33),('トルコ',34,44),('モロッコ',-9,33),('タンザニア',31,-10),('南アフリカ',25,-34),('欧州の都市部',8,57),('北米の都市部',-93,41),('オーストラリア',135,-26)]
    for name,lon,lat in labels:
        x,y=proj(lon,lat);ax.text(x,y,name,fontsize=9,ha='center',va='center',zorder=8,bbox=dict(facecolor='white',edgecolor='none',alpha=.85,pad=1.5))
    ax.set_xlim(-17800000,17800000);ax.set_ylim(-6200000,8700000);ax.set_aspect('equal');ax.axis('off')
    fig.text(.04,.085,'小国・島・都市の位置は、拡大図とCSVの地域名で確認してください。砂漠・森林を含む塗色の面積は人口密度を表しません。',fontsize=10,color='#4b5965')
    footer(fig)
    fig.savefig(OUT/'ヒジャブの出現率_世界地図.png',dpi=200,facecolor=fig.get_facecolor())
    fig.savefig(OUT/'ヒジャブの出現率_世界地図.svg',metadata={'Date':None},facecolor=fig.get_facecolor())
    tidy_svg(OUT/'ヒジャブの出現率_世界地図.svg')
    return fig

def tidy_svg(path):
    # Matplotlib adds spaces at the end of path-data lines. They are not
    # significant SVG content; retain newlines and all coordinate values.
    path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')

VIEWS=[
 ('北・西・中部アフリカ',(-19,-3,35,38),['北アフリカ','西アフリカ','中部アフリカ']),
 ('東・南部アフリカ',(26,-37,60,24),['東アフリカ','南部アフリカ']),
 ('南アジア',(44,-2,94,40),['南アジア']),
 ('インド・スリランカの位置確認',(67,5,94,36),['ISO:IND','ISO:LKA']),
 ('東南アジア',(93,-12,132,24),['東南アジア']),
 ('西・中央アジア',(25,11,76,46),['西アジア','中央アジア']),
 ('ヨーロッパ',(-8,34,56,63),['北ヨーロッパ','南ヨーロッパ','東ヨーロッパ','西ヨーロッパ']),
 ('南北アメリカ',(-125,-7,-48,58),['北アメリカ','南アメリカ','中央アメリカ','カリブ海']),
 ('オセアニア',(136,-46,180,-12),['オーストラリア・ニュージーランド','メラネシア','ミクロネシア','ポリネシア']),
]

def numbered_labels(ax,selected,extent):
    # Screen-space collision avoidance: labels retain leader lines to their points.
    fig=ax.figure;fig.canvas.draw();used=[]
    for f in selected:
        g=shape(f['geometry']);g=g.intersection(box(*extent))
        if g.is_empty:continue
        p=g if g.geom_type=='Point' else g.representative_point()
        xy=(p.x,p.y);num=NUMBERS[f['id']]
        sx,sy=ax.transData.transform(xy)
        choices=[(0,0)]+[(dx,dy) for d in [15,28,42,56,70,90] for dx,dy in [(d,0),(-d,0),(0,d),(0,-d),(d,d),(-d,d),(d,-d),(-d,-d)]]
        for dx,dy in choices:
            candidate=(sx+dx,sy+dy)
            if all(abs(candidate[0]-x)>25 or abs(candidate[1]-y)>15 for x,y in used):break
        used.append(candidate)
        dest=ax.transData.inverted().transform(candidate)
        ax.annotate(str(num),xy=xy,xytext=dest,ha='center',va='center',fontsize=8,color='#172d3d',zorder=12,bbox=dict(boxstyle='round,pad=.18',fc='white',ec='#b9c1c7',lw=.4,alpha=.97),arrowprops=dict(arrowstyle='-',color='#7b8790',lw=.45,shrinkA=1,shrinkB=1))

def atlas_page(title,extent,regions,world,features,rows,page):
    selected=[f for f in features if f['properties']['un_region_ja'] in regions or ('ISO:'+f['properties']['iso3']) in regions]
    selected_ids={f['id'] for f in selected}
    fig=plt.figure(figsize=(16,11.3),facecolor='white')
    fig.text(.04,.957,f'{page:02d}  {title}',fontsize=24,color='#172d3d',weight='bold')
    fig.text(.04,.925,'数字を右の地域一覧・CSVと対応させて覚える',fontsize=11,color='#687984')
    legend(fig,.90)
    ax=fig.add_axes([.035,.13,.56,.69],facecolor='#f3f7fa')
    basemap(ax,world,extent=extent);map_features(ax,features,extent=extent)
    ax.set_xlim(extent[0],extent[2]);ax.set_ylim(extent[1],extent[3])
    ax.set_aspect(1/max(.3,math.cos(math.radians((extent[1]+extent[3])/2))))
    ax.tick_params(labelsize=8,colors='#798793');ax.grid(lw=.3,alpha=.2)
    for sp in ax.spines.values():sp.set_color('#ccd5da')
    numbered_labels(ax,selected,extent)
    # Fixed-width Japanese text; split a dense regional list across two columns.
    entries=[r for r in rows if r['id'] in selected_ids]
    maxheight=.745;top=.834
    cols=2 if len(entries)>26 else 1
    chunks=[entries] if cols==1 else [entries[:math.ceil(len(entries)/2)],entries[math.ceil(len(entries)/2):]]
    for c,chunk in enumerate(chunks):
        x=.617+c*.19;wrap=29 if cols==1 else 14;fontsize=9.6 if cols==1 else 8.8
        wrapped=[]
        for r in chunk:
            txt=r['country_ja']+'｜'+r['area_ja'].replace('（住民の生活圏）','').replace('周辺の一部','周辺')
            ls=textwrap.wrap(txt,width=wrap,break_long_words=True,break_on_hyphens=False)
            wrapped.append((r,ls))
        linecount=sum(len(ls)+.55 for _,ls in wrapped)
        dy=min(.023,maxheight/max(linecount,1))
        y=top
        for r,ls in wrapped:
            fig.text(x,y,str(NUMBERS[r['id']]).zfill(3),fontsize=fontsize,color=COLORS[r['level']] if r['level']=='高い' else '#9a4654',weight='bold')
            for line in ls:
                fig.text(x+.027,y,line,fontsize=fontsize,color='#263b49');y-=dy
            y-=dy*.55
    footer(fig)
    fig.savefig(OUT/f'拡大図_{page:02d}.png',dpi=150)
    return fig

def main():
    setup();OUT.mkdir(exist_ok=True)
    world=json.loads((DATA/'basemap_countries.geojson').read_text())['features']
    features=json.loads((DATA/'study_regions.geojson').read_text())['features'];rows=json.loads((DATA/'study_regions.json').read_text())
    NUMBERS.update({r['id']:i+1 for i,r in enumerate(rows)})
    with PdfPages(OUT/'ヒジャブの出現率_地図帳.pdf',metadata={'Title':'ヒジャブの出現率 / GeoGuessr攻略','Author':'GeoGuessr攻略','CreationDate':None,'ModDate':None}) as pdf:
        fig=world_map(world,features);pdf.savefig(fig);plt.close(fig)
        for i,(title,extent,regions) in enumerate(VIEWS,1):
            fig=atlas_page(title,extent,regions,world,features,rows,i);pdf.savefig(fig);plt.close(fig)
    print('World PNG/SVG, regional PNGs and 10-page PDF rendered.')

if __name__=='__main__':main()
