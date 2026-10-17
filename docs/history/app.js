/* Offline explorer: reviewed labels only. No inference, network requests, or dependencies. */
(() => {
  'use strict';
  const data = window.WUI_HISTORY;
  if (!data || data.years.length !== 21 || data.years[0] !== 2001 || data.years.at(-1) !== 2021) {
    throw new Error('Expected the reviewed 2001–2021 historical snapshot.');
  }
  const $ = id => document.getElementById(id);
  const ns = 'http://www.w3.org/2000/svg';
  const ml = window.WUI_ML;
  const state = {year:2021, county:'All counties', measure:'rate', cell:null, mapMode:'observed'};
  const notify = () => document.dispatchEvent(new CustomEvent('wui:change',{detail:{...state}}));
  const summaries = new Map(data.summaries.map(row => [`${row.county}:${row.year}`, row]));
  const cells = new Map(data.cells.map(cell => [cell.id, cell]));
  const statusNames = data.status_codes;
  const number = value => value.toLocaleString('en-US');
  const percent = value => `${value.toFixed(2)}%`;
  const areaText = value => value < 0.01 ? '<0.01' : value.toFixed(2);
  const scopeCells = () => data.cells.filter(cell => state.county === 'All counties' || cell.county === state.county);
  const summary = (year = state.year) => summaries.get(`${state.county}:${year}`);
  const svgElement = (tag, attrs = {}, text = '') => {
    const element = document.createElementNS(ns, tag);
    Object.entries(attrs).forEach(([key,value]) => element.setAttribute(key, String(value)));
    if (text) element.textContent = text;
    return element;
  };
  const text = (id, value) => { $(id).textContent = value; };

  function selectYear(year) {
    if (!Number.isInteger(year) || !data.years.includes(year)) return;
    state.year = year;
    render();
  }

  function renderChart() {
    const chart = $('trend');
    chart.replaceChildren();
    const rows = data.years.map(year => summary(year));
    const values = rows.map(row => state.measure === 'rate' ? row.rate_pct : row.positive);
    const max = Math.max(...values);
    const steps = state.measure === 'rate' ? [.25,.5,1,2,5,10,20,25] : [1,2,5,10,20,25,50,100,200,500];
    const ceiling = steps.find(step => step * 4 >= max * 1.12) * 4;
    const title = svgElement('title', {id:'trend-title'}, `${state.county}: annual recorded occurrence, 2001–2021`);
    const description = svgElement('desc', {id:'trend-description'}, state.measure === 'rate'
      ? 'Percentage of known reviewed cell labels that are positive. Unknown labels are omitted; flagged zeros remain in the denominator. Each bar selects a year. Values are also available in the table.'
      : 'Number of cells with at least one recorded wildfire discovery in each year. This is not the number of fire incidents. Each bar selects a year. Values are also available in the table.');
    chart.append(title, description);
    const left=62, right=1002, top=40, bottom=276, step=(right-left)/21;
    chart.append(svgElement('text',{x:left,y:18,class:'chart-axis'},state.measure==='rate'?'Positive / known reviewed cells (%)':'Cells with ≥1 recorded wildfire discovery'));
    for (let tick=0; tick<=4; tick++) {
      const value=ceiling*tick/4, y=bottom-(bottom-top)*tick/4;
      chart.append(svgElement('line',{x1:left,x2:right,y1:y,y2:y,class:'chart-grid'}));
      chart.append(svgElement('text',{x:left-12,y:y+4,'text-anchor':'end',class:'chart-axis'},state.measure==='rate'?`${Number(value.toFixed(2))}%`:value.toFixed(0)));
    }
    const transitionX=left+19*step;
    chart.append(svgElement('rect',{x:transitionX,y:top,width:step*2,height:bottom-top,fill:'#f3eee5',opacity:.7}));
    chart.append(svgElement('line',{x1:transitionX,x2:transitionX,y1:top-7,y2:bottom,stroke:'#ab8a62','stroke-dasharray':'4 4'}));
    chart.append(svgElement('text',{x:transitionX-5,y:top-14,'text-anchor':'end',class:'chart-axis'},'2020 source transition'));
    rows.forEach((row,index) => {
      const x=left+index*step, value=values[index], height=(bottom-top)*value/ceiling;
      const label=`${row.year}: ${row.positive} positive cells; ${percent(row.rate_pct)} of ${row.known} known cells; ${row.unknown} unknown; ${row.flagged_zero} flagged zeros`;
      const group=svgElement('g',{class:'bar-group',role:'button',tabindex:'0','aria-label':label,'aria-pressed':row.year===state.year,'data-year':row.year});
      group.append(svgElement('title',{},label));
      group.append(svgElement('rect',{x:x+4,y:top-3,width:step-8,height:bottom-top+38,class:'bar-hit'}));
      group.append(svgElement('rect',{x:x+8,y:bottom-height,width:step-16,height:Math.max(height,1),rx:2,class:'bar'}));
      group.append(svgElement('text',{x:x+step/2,y:bottom+24,'text-anchor':'middle',class:'chart-axis'},String(row.year)));
      if (row.unknown || row.flagged_zero) group.append(svgElement('circle',{cx:x+step/2,cy:bottom+42,r:3,fill:'#a67d4f'}));
      group.addEventListener('click',() => selectYear(row.year));
      group.addEventListener('keydown',event => {
        if (event.key === 'Enter' || event.key === ' ') {event.preventDefault();selectYear(row.year);chart.querySelector(`[data-year="${row.year}"]`).focus();}
        if (['ArrowLeft','ArrowRight','Home','End'].includes(event.key)) {
          event.preventDefault();
          const next=event.key==='Home'?2001:event.key==='End'?2021:Math.min(2021,Math.max(2001,row.year+(event.key==='ArrowRight'?1:-1)));
          selectYear(next);chart.querySelector(`[data-year="${next}"]`).focus();
        }
      });
      chart.append(group);
    });
  }

  function initMaps() {
    data.counties.forEach((county, countyIndex) => {
      const figure=document.createElement('figure');figure.className='map-panel';figure.dataset.county=county;
      const caption=document.createElement('figcaption');
      const heading=document.createElement('h3');heading.textContent=county;
      const count=document.createElement('span');count.textContent=`${number(data.cells.filter(cell=>cell.county===county).length)} cells`;
      caption.append(heading,count);figure.append(caption);
      const map=svgElement('svg',{viewBox:'0 0 440 360',role:'group','aria-label':`${county} cells; arrow keys move through the cell list, Enter selects`});
      const defs=svgElement('defs'), pattern=svgElement('pattern',{id:`unknown-hatch-${countyIndex}`,width:6,height:6,patternUnits:'userSpaceOnUse',patternTransform:'rotate(45)'});
      pattern.append(svgElement('rect',{width:6,height:6,fill:'#e3d9c5'}),svgElement('line',{x1:0,x2:0,y1:0,y2:6,stroke:'#927a54','stroke-width':2}));defs.append(pattern);map.append(defs);
      const countyCells=data.cells.filter(cell=>cell.county===county);
      countyCells.forEach((cell,index) => {
        const path=svgElement('path',{d:cell.path,class:'cell-shape','data-cell':cell.id,tabindex:index===0?'0':'-1',role:'button','aria-label':cell.id});
        path.append(svgElement('title'));
        path.addEventListener('click',()=>selectCell(cell.id));
        path.addEventListener('keydown',event=>{
          if (event.key==='Enter'||event.key===' ') {event.preventDefault();selectCell(cell.id);}
          if (['ArrowRight','ArrowDown','ArrowLeft','ArrowUp','Home','End'].includes(event.key)) {
            event.preventDefault();
            const next=event.key==='Home'?0:event.key==='End'?countyCells.length-1:Math.max(0,Math.min(countyCells.length-1,index+(['ArrowRight','ArrowDown'].includes(event.key)?1:-1)));
            const target=map.querySelector(`[data-cell="${countyCells[next].id}"]`);
            map.querySelectorAll('[tabindex="0"]').forEach(element=>element.setAttribute('tabindex','-1'));
            target.setAttribute('tabindex','0');target.focus();
          }
        });
        map.append(path);
      });
      figure.append(map);
      const status=document.createElement('div');status.className='map-status';figure.append(status);
      $('maps').append(figure);
    });
  }

  function renderMaps() {
    text('map-year',state.year);
    $('maps').classList.toggle('single',state.county!=='All counties');
    document.querySelectorAll('.map-panel').forEach((figure,index)=>{
      const county=figure.dataset.county;figure.hidden=state.county!=='All counties'&&county!==state.county;
      const row=summaries.get(`${county}:${state.year}`);
      const available=ml.years.includes(state.year);
      const matched=available?ml.summaries.find(r=>r.county===county&&r.year===state.year):null;
      figure.querySelector('.map-status').textContent=state.mapMode==='observed'
        ? `${row.positive} positive · ${row.unknown} unknown · ${row.flagged_zero} flagged zeros`
        : !available?'No saved predictions for this year.'
        : `${matched.eligible} eligible · ${matched.unknown+matched.flagged_zero} excluded${state.mapMode==='ranking'?` · ${matched.raw_top10} saved top-decile cells`:''}`;
      figure.querySelectorAll('.cell-shape').forEach(path=>{
        const cell=cells.get(path.dataset.cell), status=cell.status[state.year-2001];
        path.setAttribute('class',`cell-shape status-${status}${cell.id===state.cell?' is-selected':''}`);
        if (status==='U') path.setAttribute('fill',`url(#unknown-hatch-${index})`); else path.removeAttribute('fill');
        let detail=statusNames[status];
        path.style.fill=status==='U'?`url(#unknown-hatch-${index})`:'';
        if(state.mapMode!=='observed') {
          const value=available?ml.cells[cell.id][state.year-2013]:null;
          path.classList.toggle('saved-top-decile',Boolean(state.mapMode==='ranking'&&value&&value[3]));
          if(!available){path.style.fill='#e9edef';detail='No saved prediction; outside 2013–2021';}
          else if(value){
            const fraction=state.mapMode==='probability'?value[0]/.4:value[2]/100;
            const t=Math.max(0,Math.min(1,fraction));
            path.style.fill=`rgb(${Math.round(238-222*t)},${Math.round(246-157*t)},${Math.round(240-146*t)})`;
            detail=state.mapMode==='probability'?`Saved conservative probability ${(100*value[0]).toFixed(2)}%`:`Saved raw rank percentile ${value[2].toFixed(1)}${value[3]?'; original annual top decile':''}`;
          } else detail=`No prediction: ${status==='U'?'unknown label':'flagged zero excluded'}`;
        }
        const label=`${cell.id}, ${state.year}: ${detail}; area ${areaText(cell.area_km2)} square kilometers`;
        path.setAttribute('aria-label',label);path.setAttribute('aria-pressed',String(cell.id===state.cell));path.querySelector('title').textContent=label;
      });
    });
  }

  function updateCellOptions() {
    $('cell-select').replaceChildren(new Option('Choose a cell from the map or list',''));
    scopeCells().forEach(cell=>$('cell-select').append(new Option(`${cell.county} · ${cell.id}`,cell.id)));
    $('cell-select').value=state.cell||'';
  }

  function selectCell(id) {
    if (id && !cells.has(id)) return;
    state.cell=id||null;$('cell-select').value=id||'';renderMaps();renderCell();
    notify();
    if (id) text('announcement',`Selected ${id}. ${statusNames[cells.get(id).status[state.year-2001]]} in ${state.year}.`);
  }

  function renderCell() {
    const detail=$('cell-detail');detail.replaceChildren();
    if (!state.cell) {
      const heading=document.createElement('h3');heading.textContent="A cell's history";
      const paragraph=document.createElement('p');paragraph.textContent='Select a cell to see all 21 annual labels and its original observation area.';detail.append(heading,paragraph);return;
    }
    const cell=cells.get(state.cell), heading=document.createElement('h3');heading.textContent=`${cell.county} · ${cell.id}`;
    const area=document.createElement('p');area.textContent=`Original footprint: ${areaText(cell.area_km2)} km²${cell.area_km2<15.999999?' · clipped boundary cell':' · effectively full cell'}${cell.cross_county?' · intersects more than one county':''}.`;
    const status=document.createElement('p');status.className='cell-status';status.textContent=`${state.year}: ${statusNames[cell.status[state.year-2001]]}`;
    const wrap=document.createElement('div');wrap.className='cell-years-wrap';const years=document.createElement('div');years.className='cell-years';years.setAttribute('role','group');years.setAttribute('aria-label','Annual labels for the selected cell');
    data.years.forEach((year,index)=>{
      const code=cell.status[index], button=document.createElement('button');button.type='button';button.className=`cell-year status-${code}`;button.dataset.cellYear=year;button.setAttribute('aria-label',`${year}: ${statusNames[code]}`);button.setAttribute('aria-pressed',String(year===state.year));button.title=`${year}: ${statusNames[code]}`;
      button.append(document.createTextNode({P:'●',N:'–',U:'?',F:'!'}[code]));const small=document.createElement('small');small.textContent=String(year).slice(2);button.append(small);
      button.addEventListener('click',()=>{selectYear(year);detail.querySelector(`[data-cell-year="${year}"]`).focus();});years.append(button);
    });wrap.append(years);detail.append(heading,area,status,wrap);
    const mlDetail=document.createElement('div');mlDetail.id='cell-ml-detail';detail.append(mlDetail);
  }

  function renderTable() {
    text('table-caption',`${state.county} · annual reviewed occurrence`);$('annual-rows').replaceChildren();
    data.years.forEach(year=>{
      const row=summary(year), tr=document.createElement('tr');if(year===state.year)tr.className='is-current';
      [year,row.positive,row.known,percent(row.rate_pct),row.unknown,row.flagged_zero].forEach((value,index)=>{
        const cell=document.createElement(index===0?'th':'td');if(index===0)cell.scope='row';cell.textContent=typeof value==='number'&&index!==0?number(value):String(value);tr.append(cell);
      });$('annual-rows').append(tr);
    });
  }

  function render() {
    const row=summary();$('year').value=state.year;text('year-output',state.year);$('previous').disabled=state.year===2001;$('next').disabled=state.year===2021;
    text('selected-heading',`${state.year} · ${state.county}`);text('selected-rate',`${percent(row.rate_pct)} of known reviewed cells`);
    text('positive',number(row.positive));text('known',number(row.known));text('unknown',number(row.unknown));text('flagged',number(row.flagged_zero));text('known-detail',`${number(row.known)} of ${number(row.cells)} study cells`);
    const context=$('year-context');context.classList.toggle('transition',state.year>=2020);
    context.textContent=state.year>=2020
      ? `${state.year} falls at or after the 2020 reporting-system transition. ${number(row.unknown)} labels are unknown in this selection. Changes in the chart cannot be attributed solely to changes in actual wildfire occurrence.`
      : row.flagged_zero?`${number(row.flagged_zero)} reviewed zeros in this year carry the frozen reconciliation flag. They remain zero labels in the historical rate; the ML evaluation excludes them. No-record labels remain subject to incomplete reporting.`
      : 'Unknown labels are omitted from the rate; known reviewed zeros remain included. A no-record label does not establish that no fire occurred. Year-to-year differences can reflect both reporting and actual occurrence.';
    renderChart();renderMaps();renderCell();renderTable();
    text('announcement',`${state.county}, ${state.year}: ${row.positive} recorded-positive cells, ${percent(row.rate_pct)} of ${row.known} known reviewed cells, ${row.unknown} unknown labels and ${row.flagged_zero} flagged zeros.`);
    notify();
  }

  $('county').addEventListener('change',event=>{state.county=event.target.value;state.cell=null;updateCellOptions();render();});
  document.querySelectorAll('input[name="measure"]').forEach(input=>input.addEventListener('change',()=>{state.measure=input.value;renderChart();notify();}));
  $('year').addEventListener('input',event=>selectYear(Number(event.target.value)));
  $('previous').addEventListener('click',()=>selectYear(state.year-1));$('next').addEventListener('click',()=>selectYear(state.year+1));
  $('cell-select').addEventListener('change',event=>selectCell(event.target.value));
  $('map-mode').addEventListener('change',event=>{state.mapMode=event.target.value;renderMaps();notify();});
  document.addEventListener('wui:requestyear',event=>selectYear(Number(event.detail)));
  initMaps();updateCellOptions();render();
})();
