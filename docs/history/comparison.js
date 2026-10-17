/* Saved development evidence only: no fitting, inference, or network requests. */
(() => {
  'use strict';
  const ml=window.WUI_ML, history=window.WUI_HISTORY;
  const $=id=>document.getElementById(id), ns='http://www.w3.org/2000/svg';
  const rows=new Map(ml.summaries.map(row=>[`${row.county}:${row.year}`,row]));
  const cells=new Map(history.cells.map(cell=>[cell.id,cell]));
  let current={year:Number($('year').value),county:$('county').value,measure:'rate',cell:null,mapMode:'observed'};
  const pct=value=>`${(100*value).toFixed(2)}%`;
  const count=value=>value.toLocaleString('en-US');
  const decimal=value=>value.toFixed(1);
  const gap=value=>`${value>0?'+':''}${value.toFixed(2)} pp`;
  const el=(tag,attrs={},text='')=>{
    const node=document.createElementNS(ns,tag);
    Object.entries(attrs).forEach(([key,value])=>node.setAttribute(key,String(value)));
    if(text)node.textContent=text;return node;
  };
  const set=(id,value)=>{$(id).textContent=value;};
  const requestYear=year=>document.dispatchEvent(new CustomEvent('wui:requestyear',{detail:year}));

  function drawChart() {
    const chart=$('ml-chart');chart.replaceChildren();
    const selected=ml.years.map(year=>rows.get(`${current.county}:${year}`));
    const raw=$('show-raw').checked, rate=current.measure==='rate';
    const value=(row,kind)=>rate?100*row[kind==='observed'?'observed_rate':kind==='conservative'?'conservative_mean':'raw_mean']
      :row[kind==='observed'?'positive':kind==='conservative'?'conservative_expected_cells':'raw_expected_cells'];
    const maximum=Math.max(...selected.flatMap(row=>[value(row,'observed'),value(row,'conservative'),...(raw?[value(row,'raw')]:[])]));
    const steps=rate?[.25,.5,1,2,5,10,20,25]:[1,2,5,10,20,25,50,100,200,500];
    const ceiling=steps.find(step=>step*4>=maximum*1.12)*4;
    const left=66,right=994,top=42,bottom=274,step=(right-left)/9;
    chart.append(el('title',{id:'ml-chart-title'},`${current.county}: matched observations and saved predictions, 2013–2021`));
    chart.append(el('desc',{id:'ml-chart-description'},'Bars show observed positive cells or occurrence rates. The solid orange line shows conservative XGBoost saved probabilities or their sum. Both use exactly the same eligible cells, excluding unknown labels and frozen flagged zeros. An optional dashed line shows the raw XGBoost reference. Each year selects the explorer year.'));
    chart.append(el('text',{x:left,y:18,class:'chart-axis'},rate?'Observed rate / mean saved probability (%)':'Observed positive cells / expected positive cells (Σp)'));
    for(let tick=0;tick<=4;tick++) {
      const y=bottom-(bottom-top)*tick/4,v=ceiling*tick/4;
      chart.append(el('line',{x1:left,x2:right,y1:y,y2:y,class:'chart-grid'}));
      chart.append(el('text',{x:left-12,y:y+4,'text-anchor':'end',class:'chart-axis'},`${Number(v.toFixed(2))}${rate?'%':''}`));
    }
    const transitionX=left+7*step;
    chart.append(el('rect',{x:transitionX,y:top,width:2*step,height:bottom-top,fill:'#f3eee5',opacity:.7}));
    chart.append(el('line',{x1:transitionX,x2:transitionX,y1:top-7,y2:bottom,stroke:'#ab8a62','stroke-dasharray':'4 4'}));
    chart.append(el('text',{x:transitionX-4,y:top-15,'text-anchor':'end',class:'chart-axis'},'2020 source transition'));
    const points={conservative:[],raw:[]};
    selected.forEach((row,index)=>{
      const x=left+(index+.5)*step;
      const observedHeight=(bottom-top)*value(row,'observed')/ceiling;
      const group=el('g',{class:'ml-year-group',role:'button',tabindex:0,'data-ml-year':row.year,
        'aria-pressed':row.year===current.year,
        'aria-label':`${row.year}: ${row.eligible} eligible cells; observed ${pct(row.observed_rate)}; conservative ${pct(row.conservative_mean)}${raw?`; raw ${pct(row.raw_mean)}`:''}`});
      group.append(el('rect',{x:x-step/2+7,y:top-4,width:step-14,height:bottom-top+42,fill:'transparent'}));
      group.append(el('rect',{x:x-19,y:bottom-observedHeight,width:38,height:Math.max(observedHeight,1),rx:2,fill:row.year===current.year?'#104f55':'#41928d'}));
      group.append(el('text',{x,y:bottom+26,'text-anchor':'middle',class:'chart-axis'},String(row.year)));
      group.append(el('title',{},`${row.year}: observed ${row.positive} / ${row.eligible}; conservative Σp ${row.conservative_expected_cells.toFixed(3)}; raw Σp ${row.raw_expected_cells.toFixed(3)}`));
      group.addEventListener('click',()=>requestYear(row.year));
      group.addEventListener('keydown',event=>{
        if(['Enter',' '].includes(event.key)){event.preventDefault();requestYear(row.year);$('ml-chart').querySelector(`[data-ml-year="${row.year}"]`).focus();}
        if(['ArrowLeft','ArrowRight','Home','End'].includes(event.key)){
          event.preventDefault();const year=event.key==='Home'?2013:event.key==='End'?2021:Math.max(2013,Math.min(2021,row.year+(event.key==='ArrowRight'?1:-1)));
          requestYear(year);$('ml-chart').querySelector(`[data-ml-year="${year}"]`).focus();
        }
      });
      chart.append(group);
      for(const kind of ['conservative','raw'])points[kind].push([x,bottom-(bottom-top)*value(row,kind)/ceiling]);
    });
    for(const kind of ['conservative',...(raw?['raw']:[])]) {
      chart.append(el('polyline',{points:points[kind].map(p=>p.join(',')).join(' '),fill:'none',stroke:kind==='conservative'?'#bd612f':'#52687e','stroke-width':2.5,'stroke-dasharray':kind==='raw'?'6 4':'none','pointer-events':'none'}));
      points[kind].forEach(([x,y])=>chart.append(el('circle',{cx:x,cy:y,r:4,fill:'white',stroke:kind==='conservative'?'#bd612f':'#52687e','stroke-width':2,'pointer-events':'none'})));
    }
    $('raw-legend').hidden=!raw;$('raw-legend-text').hidden=!raw;
  }

  function updateSummary() {
    const row=rows.get(`${current.county}:${current.year}`);
    $('ml-year').value=row?String(current.year):'';
    set('ml-selected-heading',`${current.year} · ${current.county}`);
    set('ml-available',row?'Saved geographic holdouts':'No saved predictions in this year');
    if(!row) {
      for(const id of ['ml-eligible','ml-positive','ml-expected','ml-observed','ml-predicted','ml-gap'])set(id,'—');
      set('ml-cohort',`No saved held-out predictions are available for ${current.year}. The historical view above remains available. Choose 2013–2021 here or select a year in the comparison chart.`);
      set('ml-interpretation','Earlier years supported training and calibration. They are not presented as held-out predictions.');
      set('ml-gap-note','Percentage-point difference');return;
    }
    set('ml-cohort',`Matched cohort: ${count(row.eligible)} cells in ${current.year}. Both sides omit ${count(row.unknown)} unknown labels and ${count(row.flagged_zero)} frozen flagged-zero ${row.flagged_zero === 1 ? 'label' : 'labels'}. The historical panel above retains flagged zeros, so its denominator can differ.`);
    set('ml-eligible',count(row.eligible));set('ml-positive',count(row.positive));set('ml-expected',decimal(row.conservative_expected_cells));
    set('ml-observed',pct(row.observed_rate));set('ml-predicted',pct(row.conservative_mean));set('ml-gap',gap(row.conservative_gap_pp));
    set('ml-gap-note',row.conservative_gap_pp<0?'Mean probability below observed rate':'Mean probability above observed rate');
    set('ml-interpretation',`Σp is the expected number of recorded-positive cells in this cohort, not an incident total. Observed and expected counts need not agree in a single year.${$('show-raw').checked?` Raw reference: mean ${pct(row.raw_mean)}, Σp ${decimal(row.raw_expected_cells)}.`:''} Reporting changes and real occurrence variation remain inseparable in this evidence.`);
  }

  function updateTable() {
    set('ml-table-caption',`${current.county} · saved comparison on the matched evaluation cohort`);
    $('ml-table-rows').replaceChildren();
    ml.years.forEach(year=>{
      const row=rows.get(`${current.county}:${year}`),tr=document.createElement('tr');
      if(year===current.year)tr.className='is-current';
      [year,row.eligible,row.positive,decimal(row.conservative_expected_cells),pct(row.observed_rate),pct(row.conservative_mean),pct(row.raw_mean),gap(row.conservative_gap_pp)].forEach((value,index)=>{
        const td=document.createElement(index===0?'th':'td');if(index===0)td.scope='row';td.textContent=String(value);tr.append(td);
      });$('ml-table-rows').append(tr);
    });
  }

  function updateMapLegend() {
    const mode=current.mapMode,available=ml.years.includes(current.year);
    if(mode==='observed') {
      $('map-legend').innerHTML='<li><i class="swatch status-P"></i>Recorded positive</li><li><i class="swatch status-N"></i>No recorded occurrence</li><li><i class="swatch status-U"></i>Unknown label</li><li><i class="swatch status-F"></i>Flagged zero</li>';
      set('map-title',"Locate the selected year's cells");
      set('map-view-note','Observed labels cover the full 2001–2021 historical period. Saved ML maps are available only for 2013–2021.');return;
    }
    set('map-title',mode==='probability'?'Inspect saved conservative probabilities':'Inspect the saved raw ranking');
    $('map-legend').innerHTML=available?
      `<li><i class="gradient-key"></i>${mode==='probability'?'0% → 40% probability':'0 → 100 rank percentile'}</li><li><i class="swatch status-U"></i>Unknown: no prediction</li><li><i class="swatch status-F"></i>Flagged zero: no prediction</li>${mode==='ranking'?'<li><i class="swatch top-outline"></i>Original annual top decile</li>':''}`:
      '<li><i class="swatch unavailable-key"></i>No saved predictions for this year</li>';
    set('map-view-note',!available?`No saved predictions exist for ${current.year}; gray cells mean unavailable, not zero probability.`:
      mode==='probability'?'Common 0–40% probability scale across counties and years. Missing predictions remain excluded. These maps combine geographic holdouts under the frozen specification.':
      'Rank percentiles are not probabilities. Outlines preserve the saved annual top 10% across all three counties; filtering a county does not rerank cells or create a new county budget.');
  }

  function updateCell() {
    const host=$('cell-ml-detail');if(!host||!current.cell)return;
    host.replaceChildren();const cell=cells.get(current.cell),values=ml.cells[current.cell];
    const h=document.createElement('h4');h.textContent='Saved held-out predictions · 2013–2021';host.append(h);
    const p=document.createElement('p'),value=ml.years.includes(current.year)?values[current.year-2013]:null;
    p.id='cell-ml-current';
    p.textContent=!ml.years.includes(current.year)?`${current.year}: no saved held-out prediction.`:
      !value?`${current.year}: no prediction — ${cell.status[current.year-2001]==='U'?'unknown label':'flagged zero excluded'}.`:
      `${current.year}: observed ${cell.status[current.year-2001]==='P'?'recorded positive (1)':'no recorded occurrence (0)'}; conservative probability ${pct(value[0])}; raw rank ${value[2].toFixed(1)}${value[3]?' · original annual top decile':''}.`;
    host.append(p);
    const wrap=document.createElement('div');wrap.className='table-scroll';wrap.tabIndex=0;wrap.setAttribute('role','region');wrap.setAttribute('aria-label','Saved predictions for selected cell');
    const table=document.createElement('table');table.className='cell-ml-table';
    const caption=document.createElement('caption');caption.textContent='One binary observation and its saved probability; a single outcome does not assess calibration.';table.append(caption);
    const head=document.createElement('thead'),headrow=document.createElement('tr');
    ['Year','Observed label / exclusion','Conservative probability','Raw rank percentile'].forEach(name=>{const th=document.createElement('th');th.scope='col';th.textContent=name;headrow.append(th);});head.append(headrow);table.append(head);
    const body=document.createElement('tbody');
    ml.years.forEach((year,index)=>{
      const v=values[index],code=cell.status[year-2001],tr=document.createElement('tr');if(year===current.year)tr.className='is-current';
      const th=document.createElement('th');th.scope='row';const button=document.createElement('button');button.type='button';button.className='cell-ml-year';button.dataset.predictionYear=year;button.textContent=String(year);button.setAttribute('aria-label',`Select ${year} for this cell`);
      button.addEventListener('click',()=>{requestYear(year);document.querySelector(`#cell-ml-detail [data-prediction-year="${year}"]`).focus();});th.append(button);tr.append(th);
      const labels=[code==='P'?'1 · recorded positive':code==='N'?'0 · no recorded occurrence':code==='F'?'Flagged zero · excluded':'Unknown · excluded',v?pct(v[0]):'—',v?`${v[2].toFixed(1)}${v[3]?' · top decile':''}`:'—'];
      labels.forEach(label=>{const td=document.createElement('td');td.textContent=label;tr.append(td);});body.append(tr);
    });table.append(body);wrap.append(table);host.append(wrap);
  }

  function render() {drawChart();updateSummary();updateTable();updateMapLegend();updateCell();}
  document.addEventListener('wui:change',event=>{current=event.detail;render();});
  $('ml-year').addEventListener('change',event=>{if(event.target.value)requestYear(Number(event.target.value));});
  $('show-raw').addEventListener('change',()=>{drawChart();updateSummary();});
  render();
})();
