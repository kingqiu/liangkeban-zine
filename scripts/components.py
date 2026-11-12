"""Small reusable safe-node constructors for magazine layouts. No network or execution."""
import math

def node(tag,*children,cls=None,**attrs):
 if cls:attrs['class']=cls
 return {'tag':tag,'attrs':{k:str(v) for k,v in attrs.items()},'children':list(children)}
def p(text):return node('p',text)
def h2(text):return node('h2',text)
def note(text):return node('div',text,cls='note')
def rule():return node('div',cls='rule')
def columns(left,right,equal=False):return node('div',node('div',*left),node('div',*right),cls='columns'+(' equal' if equal else ''))
def box(label,text,tone='green'):
 if tone not in {'green','purple','blue','rust'}:raise ValueError('Unsupported tone')
 return node('aside',node('div',label,cls='eyebrow'),p(text),cls='box '+tone)
def metric(value,unit='',label='',secondary=False):return node('div',node('div',str(value),node('span',unit),cls='big'+(' secondary' if secondary else '')),node('div',label,cls='metric-desc'))
def flow(items):
 if not 2<=len(items)<=4:raise ValueError('flow needs 2–4 short steps')
 return node('div',*(node('div',node('span',f'{i:02}'),v) for i,v in enumerate(items,1)),cls='arrowflow')
def number(v):
 if isinstance(v,bool) or not isinstance(v,(float,int)) or not math.isfinite(v) or v<0:raise ValueError('Chart values must be finite and nonnegative')
 return v
def bars(rows,unit='%',color='#668671'):
 values=[number(v) for _,v in rows]
 if not values or max(values)==0:raise ValueError('bars require a positive maximum')
 return node('div',*(node('div',node('span',label),node('i',style=f'width:{v/max(values)*240}px;background:{color}'),node('b',f'{v:g}{unit}'),cls='share-row') for (label,v) in rows),cls='sharebars')
def donut(percent,label):
 number(percent)
 if percent>100:raise ValueError('donut percentage must be at most 100')
 c=2*math.pi*90
 return node('svg',node('circle',cx=120,cy=120,r=90,fill='none',stroke='#d8c6b9',**{'stroke-width':31}),node('circle',cx=120,cy=120,r=90,fill='none',stroke='#668671',transform='rotate(-90 120 120)',**{'stroke-width':31,'stroke-dasharray':f'{c*percent/100} {c}'}),node('text',f'{percent:g}%',x=120,y=119,fill='#2a3430',**{'text-anchor':'middle','font-size':41,'font-weight':700}),node('text',label,x=120,y=151,fill='#637168',**{'text-anchor':'middle','font-size':16}),viewBox='0 0 240 240',role='img',**{'aria-label':f'{label} {percent:g}%'})
