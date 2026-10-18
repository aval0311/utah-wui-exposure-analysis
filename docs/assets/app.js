
    
    
            var map_d1b7ce120271f28f3680a3a773fb74bb = L.map(
                "map_d1b7ce120271f28f3680a3a773fb74bb",
                {
                    center: [38.96091422349325, -112.4552774477515],
                    crs: L.CRS.EPSG3857,
                    ...{
  "zoom": 7,
  "zoomControl": true,
  "preferCanvas": true,
}

                }
            );
            L.control.scale().addTo(map_d1b7ce120271f28f3680a3a773fb74bb);

            

        
    
            var tile_layer_5e7daf5fa750b39c4fd483a39f11e926 = L.tileLayer(
                "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
                {
  "minZoom": 0,
  "maxZoom": 19,
  "maxNativeZoom": 19,
  "noWrap": false,
  "attribution": "Tiles \u00a9 Esri",
  "subdomains": "abc",
  "detectRetina": false,
  "tms": false,
  "opacity": 1,
}

            );
        
    
            tile_layer_5e7daf5fa750b39c4fd483a39f11e926.addTo(map_d1b7ce120271f28f3680a3a773fb74bb);
        
    
            var tile_layer_1edcddab195b6aea4091802000c2bf36 = L.tileLayer(
                "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                {
  "minZoom": 0,
  "maxZoom": 19,
  "maxNativeZoom": 19,
  "noWrap": false,
  "attribution": "Imagery \u00a9 Esri",
  "subdomains": "abc",
  "detectRetina": false,
  "tms": false,
  "opacity": 1,
}

            );
        
    
            map_d1b7ce120271f28f3680a3a773fb74bb.fitBounds(
                [[36.999962312497104, -114.052896913423], [40.92186613448939, -110.85765798208]],
                {"paddingBottomRight": [20, 20], "paddingTopLeft": [20, 20]}
            );
        
    
            var feature_group_08a88c73f1e663f12f9156a14e65f217 = L.featureGroup(
                {
}
            );
        
    
        function geo_json_e219ca67f284451dfe2bb9b0f70b6ed6_styler(feature) {
            switch(feature.id) {
                default:
                    return {"color": "#374151", "fillColor": "transparent", "fillOpacity": 0.0, "opacity": 1.0, "weight": 2.0};
            }
        }
        function geo_json_e219ca67f284451dfe2bb9b0f70b6ed6_highlighter(feature) {
            switch(feature.id) {
                default:
                    return {"color": "#374151", "fillColor": "#374151", "fillOpacity": 0.1, "opacity": 1.0, "weight": 5.0};
            }
        }

        function geo_json_e219ca67f284451dfe2bb9b0f70b6ed6_onEachFeature(feature, layer) {

            layer.on({
                mouseout: function(e) {
                    if(typeof e.target.setStyle === "function"){
                            geo_json_e219ca67f284451dfe2bb9b0f70b6ed6.resetStyle(e.target);
                    }
                },
                mouseover: function(e) {
                    if(typeof e.target.setStyle === "function"){
                        const highlightStyle = geo_json_e219ca67f284451dfe2bb9b0f70b6ed6_highlighter(e.target.feature)
                        e.target.setStyle(highlightStyle);
                    }
                },
            });
        };
        var geo_json_e219ca67f284451dfe2bb9b0f70b6ed6 = L.geoJson(null, {
                onEachFeature: geo_json_e219ca67f284451dfe2bb9b0f70b6ed6_onEachFeature,
            
                style: geo_json_e219ca67f284451dfe2bb9b0f70b6ed6_styler,
            ...{
}
        });

        function geo_json_e219ca67f284451dfe2bb9b0f70b6ed6_add (data) {
            geo_json_e219ca67f284451dfe2bb9b0f70b6ed6
                .addData(data);
        }
            /* Exact geometry and attributes loaded on demand. */

        
    
    geo_json_e219ca67f284451dfe2bb9b0f70b6ed6.bindTooltip(
    function(layer){
    let div = L.DomUtil.create('div');
    
    let handleObject = feature => {
        if (feature === null) {
            return '';
        } else if (typeof(feature)=='object') {
            return JSON.stringify(feature);
        } else {
            return feature;
        }
    }
    let fields = ["COUNTY_DISPLAY_NAME"];
    let aliases = ["County:"];
    let table = '<table>' +
        String(
        fields.map(
        (v,i)=>
        `<tr>
            <th>${aliases[i].toLocaleString()}</th>
            
            <td>${handleObject(layer.feature.properties[v]).toLocaleString()}</td>
        </tr>`).join(''))
    +'</table>';
    div.innerHTML=table;
    
    return div
    }
    ,{
  "sticky": false,
  "className": "foliumtooltip",
});
                     
    
    geo_json_e219ca67f284451dfe2bb9b0f70b6ed6.bindPopup(
    function(layer){
    let div = L.DomUtil.create('div');
    
    let handleObject = feature => {
        if (feature === null) {
            return '';
        } else if (typeof(feature)=='object') {
            return JSON.stringify(feature);
        } else {
            return feature;
        }
    }
    let fields = ["COUNTY_DISPLAY_NAME"];
    let aliases = ["County:"];
    let table = '<table>' +
        String(
        fields.map(
        (v,i)=>
        `<tr>
            <th>${aliases[i].toLocaleString()}</th>
            
            <td>${handleObject(layer.feature.properties[v]).toLocaleString()}</td>
        </tr>`).join(''))
    +'</table>';
    div.innerHTML=table;
    
    return div
    }
    ,{
  "className": "foliumpopup",
});
                     
    
            geo_json_e219ca67f284451dfe2bb9b0f70b6ed6.addTo(feature_group_08a88c73f1e663f12f9156a14e65f217);
        
    
            feature_group_08a88c73f1e663f12f9156a14e65f217.addTo(map_d1b7ce120271f28f3680a3a773fb74bb);
        
    
            var feature_group_5dc82d5dc5d86b36554fc9189fd11c3f = L.featureGroup(
                {
}
            );
        
    
        function geo_json_e6cbce1cc23c42f8856060f9c9f015e8_styler(feature) {
            switch(feature.id) {
                default:
                    return {"color": "#374151", "fillColor": "transparent", "fillOpacity": 0.0, "opacity": 1.0, "weight": 2.0};
            }
        }
        function geo_json_e6cbce1cc23c42f8856060f9c9f015e8_highlighter(feature) {
            switch(feature.id) {
                default:
                    return {"color": "#374151", "fillColor": "#374151", "fillOpacity": 0.1, "opacity": 1.0, "weight": 5.0};
            }
        }

        function geo_json_e6cbce1cc23c42f8856060f9c9f015e8_onEachFeature(feature, layer) {

            layer.on({
                mouseout: function(e) {
                    if(typeof e.target.setStyle === "function"){
                            geo_json_e6cbce1cc23c42f8856060f9c9f015e8.resetStyle(e.target);
                    }
                },
                mouseover: function(e) {
                    if(typeof e.target.setStyle === "function"){
                        const highlightStyle = geo_json_e6cbce1cc23c42f8856060f9c9f015e8_highlighter(e.target.feature)
                        e.target.setStyle(highlightStyle);
                    }
                },
            });
        };
        var geo_json_e6cbce1cc23c42f8856060f9c9f015e8 = L.geoJson(null, {
                onEachFeature: geo_json_e6cbce1cc23c42f8856060f9c9f015e8_onEachFeature,
            
                style: geo_json_e6cbce1cc23c42f8856060f9c9f015e8_styler,
            ...{
}
        });

        function geo_json_e6cbce1cc23c42f8856060f9c9f015e8_add (data) {
            geo_json_e6cbce1cc23c42f8856060f9c9f015e8
                .addData(data);
        }
            /* Exact geometry and attributes loaded on demand. */

        
    
    geo_json_e6cbce1cc23c42f8856060f9c9f015e8.bindTooltip(
    function(layer){
    let div = L.DomUtil.create('div');
    
    let handleObject = feature => {
        if (feature === null) {
            return '';
        } else if (typeof(feature)=='object') {
            return JSON.stringify(feature);
        } else {
            return feature;
        }
    }
    let fields = ["COUNTY_DISPLAY_NAME"];
    let aliases = ["County:"];
    let table = '<table>' +
        String(
        fields.map(
        (v,i)=>
        `<tr>
            <th>${aliases[i].toLocaleString()}</th>
            
            <td>${handleObject(layer.feature.properties[v]).toLocaleString()}</td>
        </tr>`).join(''))
    +'</table>';
    div.innerHTML=table;
    
    return div
    }
    ,{
  "sticky": false,
  "className": "foliumtooltip",
});
                     
    
    geo_json_e6cbce1cc23c42f8856060f9c9f015e8.bindPopup(
    function(layer){
    let div = L.DomUtil.create('div');
    
    let handleObject = feature => {
        if (feature === null) {
            return '';
        } else if (typeof(feature)=='object') {
            return JSON.stringify(feature);
        } else {
            return feature;
        }
    }
    let fields = ["COUNTY_DISPLAY_NAME"];
    let aliases = ["County:"];
    let table = '<table>' +
        String(
        fields.map(
        (v,i)=>
        `<tr>
            <th>${aliases[i].toLocaleString()}</th>
            
            <td>${handleObject(layer.feature.properties[v]).toLocaleString()}</td>
        </tr>`).join(''))
    +'</table>';
    div.innerHTML=table;
    
    return div
    }
    ,{
  "className": "foliumpopup",
});
                     
    
            geo_json_e6cbce1cc23c42f8856060f9c9f015e8.addTo(feature_group_5dc82d5dc5d86b36554fc9189fd11c3f);
        
    
            feature_group_5dc82d5dc5d86b36554fc9189fd11c3f.addTo(map_d1b7ce120271f28f3680a3a773fb74bb);
        
    
            var feature_group_a5b3848c21960057590945d931e8abac = L.featureGroup(
                {
}
            );
        
    
        function geo_json_352e79a818e7f6adb399345209edd260_styler(feature) {
            switch(feature.id) {
                default:
                    return {"color": "#374151", "fillColor": "transparent", "fillOpacity": 0.0, "opacity": 1.0, "weight": 2.0};
            }
        }
        function geo_json_352e79a818e7f6adb399345209edd260_highlighter(feature) {
            switch(feature.id) {
                default:
                    return {"color": "#374151", "fillColor": "#374151", "fillOpacity": 0.1, "opacity": 1.0, "weight": 5.0};
            }
        }

        function geo_json_352e79a818e7f6adb399345209edd260_onEachFeature(feature, layer) {

            layer.on({
                mouseout: function(e) {
                    if(typeof e.target.setStyle === "function"){
                            geo_json_352e79a818e7f6adb399345209edd260.resetStyle(e.target);
                    }
                },
                mouseover: function(e) {
                    if(typeof e.target.setStyle === "function"){
                        const highlightStyle = geo_json_352e79a818e7f6adb399345209edd260_highlighter(e.target.feature)
                        e.target.setStyle(highlightStyle);
                    }
                },
            });
        };
        var geo_json_352e79a818e7f6adb399345209edd260 = L.geoJson(null, {
                onEachFeature: geo_json_352e79a818e7f6adb399345209edd260_onEachFeature,
            
                style: geo_json_352e79a818e7f6adb399345209edd260_styler,
            ...{
}
        });

        function geo_json_352e79a818e7f6adb399345209edd260_add (data) {
            geo_json_352e79a818e7f6adb399345209edd260
                .addData(data);
        }
            /* Exact geometry and attributes loaded on demand. */

        
    
    geo_json_352e79a818e7f6adb399345209edd260.bindTooltip(
    function(layer){
    let div = L.DomUtil.create('div');
    
    let handleObject = feature => {
        if (feature === null) {
            return '';
        } else if (typeof(feature)=='object') {
            return JSON.stringify(feature);
        } else {
            return feature;
        }
    }
    let fields = ["COUNTY_DISPLAY_NAME"];
    let aliases = ["County:"];
    let table = '<table>' +
        String(
        fields.map(
        (v,i)=>
        `<tr>
            <th>${aliases[i].toLocaleString()}</th>
            
            <td>${handleObject(layer.feature.properties[v]).toLocaleString()}</td>
        </tr>`).join(''))
    +'</table>';
    div.innerHTML=table;
    
    return div
    }
    ,{
  "sticky": false,
  "className": "foliumtooltip",
});
                     
    
    geo_json_352e79a818e7f6adb399345209edd260.bindPopup(
    function(layer){
    let div = L.DomUtil.create('div');
    
    let handleObject = feature => {
        if (feature === null) {
            return '';
        } else if (typeof(feature)=='object') {
            return JSON.stringify(feature);
        } else {
            return feature;
        }
    }
    let fields = ["COUNTY_DISPLAY_NAME"];
    let aliases = ["County:"];
    let table = '<table>' +
        String(
        fields.map(
        (v,i)=>
        `<tr>
            <th>${aliases[i].toLocaleString()}</th>
            
            <td>${handleObject(layer.feature.properties[v]).toLocaleString()}</td>
        </tr>`).join(''))
    +'</table>';
    div.innerHTML=table;
    
    return div
    }
    ,{
  "className": "foliumpopup",
});
                     
    
            geo_json_352e79a818e7f6adb399345209edd260.addTo(feature_group_a5b3848c21960057590945d931e8abac);
        
    
            feature_group_a5b3848c21960057590945d931e8abac.addTo(map_d1b7ce120271f28f3680a3a773fb74bb);
        
    
            var feature_group_1d34b2bd2307238c7a702a70b8c84f3c = L.featureGroup(
                {
}
            );
        
    
        function geo_json_c4ce6f29e558d75ea8c8ad5e2241d1ce_styler(feature) {
            switch(feature.id) {
                default:
                    return {"color": "#6d28d9", "fillColor": "#8b5cf6", "fillOpacity": 0.1, "opacity": 0.9, "weight": 1.8};
            }
        }
        function geo_json_c4ce6f29e558d75ea8c8ad5e2241d1ce_highlighter(feature) {
            switch(feature.id) {
                default:
                    return {"color": "#4c1d95", "fillColor": "#a78bfa", "fillOpacity": 0.24, "opacity": 1.0, "weight": 2.5};
            }
        }

        function geo_json_c4ce6f29e558d75ea8c8ad5e2241d1ce_onEachFeature(feature, layer) {

            layer.on({
                mouseout: function(e) {
                    if(typeof e.target.setStyle === "function"){
                            geo_json_c4ce6f29e558d75ea8c8ad5e2241d1ce.resetStyle(e.target);
                    }
                },
                mouseover: function(e) {
                    if(typeof e.target.setStyle === "function"){
                        const highlightStyle = geo_json_c4ce6f29e558d75ea8c8ad5e2241d1ce_highlighter(e.target.feature)
                        e.target.setStyle(highlightStyle);
                    }
                },
            });
        };
        var geo_json_c4ce6f29e558d75ea8c8ad5e2241d1ce = L.geoJson(null, {
                onEachFeature: geo_json_c4ce6f29e558d75ea8c8ad5e2241d1ce_onEachFeature,
            
                style: geo_json_c4ce6f29e558d75ea8c8ad5e2241d1ce_styler,
            ...{
}
        });

        function geo_json_c4ce6f29e558d75ea8c8ad5e2241d1ce_add (data) {
            geo_json_c4ce6f29e558d75ea8c8ad5e2241d1ce
                .addData(data);
        }
            /* Exact geometry and attributes loaded on demand. */

        
    
    geo_json_c4ce6f29e558d75ea8c8ad5e2241d1ce.bindTooltip(
    function(layer){
    let div = L.DomUtil.create('div');
    
    let handleObject = feature => {
        if (feature === null) {
            return '';
        } else if (typeof(feature)=='object') {
            return JSON.stringify(feature);
        } else {
            return feature;
        }
    }
    let fields = ["WUI_POLYGON_ID", "COUNTY_NAME", "WUI_AREA_KM2"];
    let aliases = ["WUI Polygon:", "County:", "Area (km\u00b2):"];
    let table = '<table>' +
        String(
        fields.map(
        (v,i)=>
        `<tr>
            <th>${aliases[i].toLocaleString()}</th>
            
            <td>${handleObject(layer.feature.properties[v]).toLocaleString()}</td>
        </tr>`).join(''))
    +'</table>';
    div.innerHTML=table;
    
    return div
    }
    ,{
  "sticky": false,
  "className": "foliumtooltip",
});
                     
    
    geo_json_c4ce6f29e558d75ea8c8ad5e2241d1ce.bindPopup(
    function(layer){
    let div = L.DomUtil.create('div');
    
    let handleObject = feature => {
        if (feature === null) {
            return '';
        } else if (typeof(feature)=='object') {
            return JSON.stringify(feature);
        } else {
            return feature;
        }
    }
    let fields = ["WUI_POLYGON_ID", "COUNTY_NAME", "WUI_AREA_KM2"];
    let aliases = ["WUI Polygon ID:", "Intersecting County:", "Polygon Area (km\u00b2):"];
    let table = '<table>' +
        String(
        fields.map(
        (v,i)=>
        `<tr>
            <th>${aliases[i].toLocaleString()}</th>
            
            <td>${handleObject(layer.feature.properties[v]).toLocaleString()}</td>
        </tr>`).join(''))
    +'</table>';
    div.innerHTML=table;
    
    return div
    }
    ,{
  "className": "foliumpopup",
});
                     
    
            geo_json_c4ce6f29e558d75ea8c8ad5e2241d1ce.addTo(feature_group_1d34b2bd2307238c7a702a70b8c84f3c);
        
    
            
        
    
            var feature_group_738a8bd9e920586fc11716d9f694f329 = L.featureGroup(
                {
}
            );
        
    
        function geo_json_3171758a9cc9684c2da02e0a1928d3e0_styler(feature) {
            switch(feature.id) {
                case "0": case "1": case "2": case "3": case "4": case "5": case "6": case "7": case "8": case "9": case "10": case "13": case "14": case "15": case "16": case "17": case "18": case "19": case "21": case "22": case "23": case "25": case "26": case "27": case "29": case "31": case "32": case "33": case "34": case "35": case "36": case "37": case "38": case "39": case "40": case "41": case "42": case "43": case "44": case "45": case "46": case "47": case "48": case "49": case "50": case "51": case "52": case "53": case "54": case "55": case "56": case "57": case "58": case "59": case "60": case "61": case "62": case "63": case "64": case "65": case "66": case "67": case "68": case "69": case "70": case "71": case "72": case "73": case "74": case "75": case "76": case "77": case "78": case "79": case "80": case "81": case "82": case "83": case "84": case "85": case "86": case "87": case "88": case "89": case "90": case "91": case "92": case "93": case "94": case "95": case "97": case "98": case "99": case "100": case "101": case "102": case "103": case "104": case "105": case "106": case "107": case "108": case "109": case "110": case "111": case "112": case "113": case "114": case "115": case "116": case "117": case "118": case "119": case "120": case "121": case "122": case "123": case "124": case "125": case "126": case "127": case "128": case "129": case "130": case "131": case "132": case "133": case "134": case "135": case "136": case "137": case "138": case "139": case "140": case "141": case "142": case "143": case "144": case "145": case "146": case "147": case "148": case "149": case "150": case "151": case "152": case "153": case "154": case "155": case "156": case "157": case "158": case "159": case "160": case "161": case "162": case "163": case "164": case "167": case "168": case "169": case "170": case "171": case "172": case "173": case "174": case "175": case "176": case "177": case "178": case "179": case "180": case "181": case "182": case "183": case "184": case "185": case "186": case "187": case "188": case "189": case "191": case "193": case "194": case "195": case "196": case "197": case "198": case "199": case "200": case "201": case "202": case "203": case "204": case "205": case "206": case "207": case "208": case "209": case "210": case "211": case "212": case "213": case "214": case "215": case "216": case "217": case "218": case "219": case "220": case "221": case "222": case "223": case "224": case "225": case "226": case "227": case "228": case "229": case "230": case "231": case "232": case "233": case "234": case "235": case "236": case "237": case "238": case "239": case "240": case "241": case "242": case "243": case "244": case "245": case "246": case "247": case "248": case "249": case "250": case "251": case "252": case "253": case "254": case "255": case "256": case "257": case "258": case "259": case "260": case "261": case "262": case "263": case "264": case "265": case "266": case "267": case "268": case "269": case "270": case "271": case "272": case "273": case "274": case "275": case "276": case "277": case "278": case "279": case "280": case "281": case "282": case "283": case "284": case "285": case "286": case "287": case "288": case "289": case "290": case "291": case "292": case "293": case "294": case "295": case "296": case "297": case "298": case "299": case "300": case "301": case "302": case "303": case "304": case "305": case "306": case "307": case "308": case "309": case "310": case "311": case "312": case "313": case "314": case "315": case "316": case "317": case "318": case "319": case "320": case "321": case "322": case "323": case "324": case "325": case "326": case "327": case "328": case "329": case "330": case "331": case "332": case "333": case "334": case "335": case "336": case "337": case "338": case "339": case "340": case "341": case "342": case "343": case "344": case "345": case "346": case "347": case "348": case "349": case "350": case "351": case "352": case "353": case "354": case "355": case "356": case "357": case "358": case "359": case "360": case "361": case "362": case "363": case "364": case "365": case "366": case "367": case "368": case "369": case "370": case "371": case "372": case "373": case "374": case "375": case "376": case "377": case "378": case "379": case "380": case "381": case "382": case "383": case "384": case "385": case "386": case "387": case "388": case "389": case "390": case "391": case "392": case "393": case "394": case "396": case "397": case "398": case "399": case "400": case "401": case "402": case "403": case "404": case "405": case "406": case "407": case "408": case "409": case "410": case "411": case "412": case "413": case "414": case "415": case "416": case "417": case "418": case "419": case "420": case "421": case "422": case "423": case "424": case "425": case "426": case "427": case "428": case "429": case "430": case "431": case "432": case "433": case "434": case "435": case "436": case "437": case "438": case "439": case "440": case "441": case "442": case "443": case "444": case "445": case "446": case "447": case "448": case "449": case "450": case "451": case "452": case "453": case "454": case "455": case "456": case "457": case "458": case "459": case "460": case "461": case "462": case "463": case "464": case "465": case "466": case "469": case "470": case "471": case "472": case "473": case "474": case "475": case "476": case "477": case "478": case "479": case "480": case "482": case "483": case "484": case "485": case "486": case "487": case "488": case "489": case "490": case "491": case "492": case "493": case "494": case "495": case "496": case "497": case "498": case "499": case "500": case "501": case "502": case "503": case "504": case "505": case "506": case "507": case "508": case "509": case "510": case "511": case "512": case "513": case "514": case "515": case "516": case "517": case "518": case "519": case "520": case "521": case "522": case "523": case "524": case "525": case "526": case "527": case "529": case "530": case "531": case "532": case "533": case "534": case "535": case "537": case "538": case "539": case "540": case "541": case "542": case "543": case "544": case "545": case "546": case "547": case "548": case "549": case "550": case "551": case "552": case "553": case "554": case "555": case "556": case "557": case "558": case "559": case "560": case "561": case "562": case "563": case "564": case "565": case "566": case "567": case "568": case "569": case "570": case "571": case "572": case "573": case "574": case "575": case "576": case "577": case "578": case "579": case "580": case "581": case "582": case "583": case "584": case "585": case "586": case "587": case "588": case "589": case "590": case "591": case "592": case "593": case "594": case "595": case "596": case "597": case "598": case "599": case "600": case "601": case "602": case "603": case "604": case "605": case "606": case "607": case "608": case "609": case "610": case "611": case "612": case "613": case "614": case "615": case "616": case "617": case "618": case "619": case "620": case "621": case "622": case "623": case "624": case "625": case "626": case "627": case "628": case "629": case "630": case "631": case "632": case "633": case "634": case "635": case "636": case "637": case "638": case "639": case "640": case "641": case "642": case "643": case "644": case "645": case "646": case "647": case "648": case "649": case "650": case "651": case "652": case "653": case "654": case "655": case "656": case "657": case "658": case "659": case "660": case "661": case "662": case "663": case "664": case "665": case "666": case "667": case "668": case "669": case "670": case "671": case "672": case "673": case "674": case "675": case "676": case "677": case "678": case "679": case "680": case "681": case "682": case "683": case "684": case "685": case "686": case "687": case "688": case "689": case "690": case "691": case "692": case "693": case "694": case "696": case "698": case "699": case "700": case "702": case "703": case "704": case "705": case "706": case "707": case "708": case "709": case "710": case "711": case "712": case "714": case "715": case "716": case "717": case "718": case "719": case "720": case "721": case "722": case "723": case "724": case "726": case "727": case "728": case "729": case "730": case "731": case "732": case "733": case "734": case "735": case "736": case "737": case "739": case "740": case "741": case "742": case "743": case "744": case "745": case "746": case "747": case "748": case "749": case "750": case "752": case "753": case "754": case "755": case "757": case "758": case "759": case "760": case "761": case "762": case "763": case "764": case "765": case "766": case "767": case "768": case "769": case "770": case "771": case "772": case "773": case "774": case "775": case "776": case "778": case "779": case "781": case "782": case "783": case "790": case "791": case "792": case "793": case "794": case "795": case "796": case "797": case "798": case "799": case "800": case "801": case "802": case "803": case "804": case "805": case "806": case "807": case "809": case "810": case "811": case "812": case "813": case "814": case "815": case "816": case "817": case "818": case "819": case "820": case "821": case "822": case "823": case "824": case "825": case "826": case "827": case "828": case "829": case "830": case "831": case "832": case "833": case "834": case "835": case "836": case "837": case "839": case "840": case "841": case "842": case "843": case "845": case "846": case "847": case "848": case "849": case "850": case "851": case "852": case "853": case "854": case "855": case "856": case "857": case "858": case "859": case "860": case "861": case "862": case "863": case "864": case "865": case "866": case "867": case "868": case "869": case "870": case "872": case "874": case "875": case "876": case "878": case "880": case "881": case "882": case "883": case "884": case "888": case "889": case "890": case "891": case "892": case "893": case "894": case "895": case "896": case "897": case "898": case "899": case "900": case "901": case "902": case "903": case "905": case "906": case "907": case "908": case "910": case "911": case "914": case "916": case "917": case "918": case "919": case "920": case "921": case "926": case "927": case "929": case "930": case "931": case "932": case "933": case "934": case "936": case "937": case "938": case "939": case "940": case "941": case "942": case "943": case "944": case "945": case "946": case "947": case "948": case "949": case "950": case "951": case "952": case "953": case "954": case "955": case "956": case "957": case "958": case "959": case "960": case "961": case "962": case "963": case "964": case "965": case "967": case "968": case "969": case "970": case "971": case "972": case "973": case "974": case "975": case "976": case "977": case "978": case "979": case "980": case "981": case "982": case "983": case "984": case "985": case "986": case "987": case "988": case "989": case "990": case "991": case "992": case "993": case "994": case "995": case "996": case "997": case "998": case "1000": case "1001": case "1002": case "1003": case "1004": case "1005": case "1006": case "1007": case "1008": case "1009": case "1010": case "1011": case "1012": case "1013": case "1014": case "1015": case "1016": case "1017": case "1018": case "1019": case "1020": case "1021": case "1022": case "1023": case "1024": case "1026": case "1028": case "1029": case "1032": case "1033": case "1034": case "1035": case "1036": case "1037": case "1038": case "1039": case "1040": case "1041": case "1042": case "1043": case "1044": case "1045": case "1046": case "1047": case "1048": case "1049": case "1050": case "1051": case "1052": case "1053": case "1054": case "1055": case "1056": case "1057": case "1058": case "1059": case "1060": case "1061": case "1062": case "1063": case "1064": case "1065": case "1066": case "1067": case "1068": case "1069": case "1070": case "1071": case "1072": case "1073": case "1074": case "1075": case "1076": case "1077": case "1078": case "1079": case "1080": case "1081": case "1082": case "1083": case "1084": case "1085": case "1086": case "1087": case "1088": case "1089": case "1090": case "1091": case "1092": case "1093": case "1095": case "1096": case "1097": case "1098": case "1099": case "1100": case "1101": case "1102": case "1103": case "1104": case "1105": case "1106": case "1107": case "1108": case "1109": case "1110": case "1111": case "1112": case "1113": case "1114": case "1115": case "1116": case "1117": case "1118": case "1119": case "1120": case "1121": case "1122": case "1123": case "1124": case "1125": case "1126": case "1127": case "1128": case "1129": case "1131": case "1132": case "1133": case "1134": case "1137": case "1138": case "1139": case "1140": case "1141": case "1143": case "1144": case "1145": case "1150": case "1151": case "1152": case "1153": case "1154": case "1156": case "1160": case "1164": case "1166": case "1167": case "1168": case "1169": case "1171": case "1174": case "1180": case "1182": case "1185": case "1188": case "1190": case "1191": case "1192": case "1193": case "1195": case "1196": case "1197": case "1198": case "1200": case "1201": case "1204": case "1205": case "1206": case "1208": case "1209": case "1211": case "1212": case "1213": case "1214": case "1215": case "1220": case "1221": case "1222": case "1227": case "1229": case "1230": case "1231": case "1232": case "1237": case "1238": 
                    return {"color": "#4b5563", "fillColor": "#f7fbff", "fillOpacity": 0.6, "opacity": 0.75, "weight": 0.6};
                case "11": case "12": case "395": case "1203": case "1219": 
                    return {"color": "#4b5563", "fillColor": "#fc8d59", "fillOpacity": 0.6, "opacity": 0.75, "weight": 0.6};
                case "20": case "166": case "192": case "481": case "697": case "713": case "725": case "786": case "788": case "808": case "844": case "871": case "912": case "913": case "1155": case "1157": case "1158": case "1161": case "1175": case "1176": case "1177": case "1181": case "1187": case "1216": 
                    return {"color": "#4b5563", "fillColor": "#fdbb84", "fillOpacity": 0.6, "opacity": 0.75, "weight": 0.6};
                default:
                    return {"color": "#4b5563", "fillColor": "#fee8c8", "fillOpacity": 0.6, "opacity": 0.75, "weight": 0.6};
            }
        }
        function geo_json_3171758a9cc9684c2da02e0a1928d3e0_highlighter(feature) {
            switch(feature.id) {
                case "0": case "1": case "2": case "3": case "4": case "5": case "6": case "7": case "8": case "9": case "10": case "13": case "14": case "15": case "16": case "17": case "18": case "19": case "21": case "22": case "23": case "25": case "26": case "27": case "29": case "31": case "32": case "33": case "34": case "35": case "36": case "37": case "38": case "39": case "40": case "41": case "42": case "43": case "44": case "45": case "46": case "47": case "48": case "49": case "50": case "51": case "52": case "53": case "54": case "55": case "56": case "57": case "58": case "59": case "60": case "61": case "62": case "63": case "64": case "65": case "66": case "67": case "68": case "69": case "70": case "71": case "72": case "73": case "74": case "75": case "76": case "77": case "78": case "79": case "80": case "81": case "82": case "83": case "84": case "85": case "86": case "87": case "88": case "89": case "90": case "91": case "92": case "93": case "94": case "95": case "97": case "98": case "99": case "100": case "101": case "102": case "103": case "104": case "105": case "106": case "107": case "108": case "109": case "110": case "111": case "112": case "113": case "114": case "115": case "116": case "117": case "118": case "119": case "120": case "121": case "122": case "123": case "124": case "125": case "126": case "127": case "128": case "129": case "130": case "131": case "132": case "133": case "134": case "135": case "136": case "137": case "138": case "139": case "140": case "141": case "142": case "143": case "144": case "145": case "146": case "147": case "148": case "149": case "150": case "151": case "152": case "153": case "154": case "155": case "156": case "157": case "158": case "159": case "160": case "161": case "162": case "163": case "164": case "167": case "168": case "169": case "170": case "171": case "172": case "173": case "174": case "175": case "176": case "177": case "178": case "179": case "180": case "181": case "182": case "183": case "184": case "185": case "186": case "187": case "188": case "189": case "191": case "193": case "194": case "195": case "196": case "197": case "198": case "199": case "200": case "201": case "202": case "203": case "204": case "205": case "206": case "207": case "208": case "209": case "210": case "211": case "212": case "213": case "214": case "215": case "216": case "217": case "218": case "219": case "220": case "221": case "222": case "223": case "224": case "225": case "226": case "227": case "228": case "229": case "230": case "231": case "232": case "233": case "234": case "235": case "236": case "237": case "238": case "239": case "240": case "241": case "242": case "243": case "244": case "245": case "246": case "247": case "248": case "249": case "250": case "251": case "252": case "253": case "254": case "255": case "256": case "257": case "258": case "259": case "260": case "261": case "262": case "263": case "264": case "265": case "266": case "267": case "268": case "269": case "270": case "271": case "272": case "273": case "274": case "275": case "276": case "277": case "278": case "279": case "280": case "281": case "282": case "283": case "284": case "285": case "286": case "287": case "288": case "289": case "290": case "291": case "292": case "293": case "294": case "295": case "296": case "297": case "298": case "299": case "300": case "301": case "302": case "303": case "304": case "305": case "306": case "307": case "308": case "309": case "310": case "311": case "312": case "313": case "314": case "315": case "316": case "317": case "318": case "319": case "320": case "321": case "322": case "323": case "324": case "325": case "326": case "327": case "328": case "329": case "330": case "331": case "332": case "333": case "334": case "335": case "336": case "337": case "338": case "339": case "340": case "341": case "342": case "343": case "344": case "345": case "346": case "347": case "348": case "349": case "350": case "351": case "352": case "353": case "354": case "355": case "356": case "357": case "358": case "359": case "360": case "361": case "362": case "363": case "364": case "365": case "366": case "367": case "368": case "369": case "370": case "371": case "372": case "373": case "374": case "375": case "376": case "377": case "378": case "379": case "380": case "381": case "382": case "383": case "384": case "385": case "386": case "387": case "388": case "389": case "390": case "391": case "392": case "393": case "394": case "396": case "397": case "398": case "399": case "400": case "401": case "402": case "403": case "404": case "405": case "406": case "407": case "408": case "409": case "410": case "411": case "412": case "413": case "414": case "415": case "416": case "417": case "418": case "419": case "420": case "421": case "422": case "423": case "424": case "425": case "426": case "427": case "428": case "429": case "430": case "431": case "432": case "433": case "434": case "435": case "436": case "437": case "438": case "439": case "440": case "441": case "442": case "443": case "444": case "445": case "446": case "447": case "448": case "449": case "450": case "451": case "452": case "453": case "454": case "455": case "456": case "457": case "458": case "459": case "460": case "461": case "462": case "463": case "464": case "465": case "466": case "469": case "470": case "471": case "472": case "473": case "474": case "475": case "476": case "477": case "478": case "479": case "480": case "482": case "483": case "484": case "485": case "486": case "487": case "488": case "489": case "490": case "491": case "492": case "493": case "494": case "495": case "496": case "497": case "498": case "499": case "500": case "501": case "502": case "503": case "504": case "505": case "506": case "507": case "508": case "509": case "510": case "511": case "512": case "513": case "514": case "515": case "516": case "517": case "518": case "519": case "520": case "521": case "522": case "523": case "524": case "525": case "526": case "527": case "529": case "530": case "531": case "532": case "533": case "534": case "535": case "537": case "538": case "539": case "540": case "541": case "542": case "543": case "544": case "545": case "546": case "547": case "548": case "549": case "550": case "551": case "552": case "553": case "554": case "555": case "556": case "557": case "558": case "559": case "560": case "561": case "562": case "563": case "564": case "565": case "566": case "567": case "568": case "569": case "570": case "571": case "572": case "573": case "574": case "575": case "576": case "577": case "578": case "579": case "580": case "581": case "582": case "583": case "584": case "585": case "586": case "587": case "588": case "589": case "590": case "591": case "592": case "593": case "594": case "595": case "596": case "597": case "598": case "599": case "600": case "601": case "602": case "603": case "604": case "605": case "606": case "607": case "608": case "609": case "610": case "611": case "612": case "613": case "614": case "615": case "616": case "617": case "618": case "619": case "620": case "621": case "622": case "623": case "624": case "625": case "626": case "627": case "628": case "629": case "630": case "631": case "632": case "633": case "634": case "635": case "636": case "637": case "638": case "639": case "640": case "641": case "642": case "643": case "644": case "645": case "646": case "647": case "648": case "649": case "650": case "651": case "652": case "653": case "654": case "655": case "656": case "657": case "658": case "659": case "660": case "661": case "662": case "663": case "664": case "665": case "666": case "667": case "668": case "669": case "670": case "671": case "672": case "673": case "674": case "675": case "676": case "677": case "678": case "679": case "680": case "681": case "682": case "683": case "684": case "685": case "686": case "687": case "688": case "689": case "690": case "691": case "692": case "693": case "694": case "696": case "698": case "699": case "700": case "702": case "703": case "704": case "705": case "706": case "707": case "708": case "709": case "710": case "711": case "712": case "714": case "715": case "716": case "717": case "718": case "719": case "720": case "721": case "722": case "723": case "724": case "726": case "727": case "728": case "729": case "730": case "731": case "732": case "733": case "734": case "735": case "736": case "737": case "739": case "740": case "741": case "742": case "743": case "744": case "745": case "746": case "747": case "748": case "749": case "750": case "752": case "753": case "754": case "755": case "757": case "758": case "759": case "760": case "761": case "762": case "763": case "764": case "765": case "766": case "767": case "768": case "769": case "770": case "771": case "772": case "773": case "774": case "775": case "776": case "778": case "779": case "781": case "782": case "783": case "790": case "791": case "792": case "793": case "794": case "795": case "796": case "797": case "798": case "799": case "800": case "801": case "802": case "803": case "804": case "805": case "806": case "807": case "809": case "810": case "811": case "812": case "813": case "814": case "815": case "816": case "817": case "818": case "819": case "820": case "821": case "822": case "823": case "824": case "825": case "826": case "827": case "828": case "829": case "830": case "831": case "832": case "833": case "834": case "835": case "836": case "837": case "839": case "840": case "841": case "842": case "843": case "845": case "846": case "847": case "848": case "849": case "850": case "851": case "852": case "853": case "854": case "855": case "856": case "857": case "858": case "859": case "860": case "861": case "862": case "863": case "864": case "865": case "866": case "867": case "868": case "869": case "870": case "872": case "874": case "875": case "876": case "878": case "880": case "881": case "882": case "883": case "884": case "888": case "889": case "890": case "891": case "892": case "893": case "894": case "895": case "896": case "897": case "898": case "899": case "900": case "901": case "902": case "903": case "905": case "906": case "907": case "908": case "910": case "911": case "914": case "916": case "917": case "918": case "919": case "920": case "921": case "926": case "927": case "929": case "930": case "931": case "932": case "933": case "934": case "936": case "937": case "938": case "939": case "940": case "941": case "942": case "943": case "944": case "945": case "946": case "947": case "948": case "949": case "950": case "951": case "952": case "953": case "954": case "955": case "956": case "957": case "958": case "959": case "960": case "961": case "962": case "963": case "964": case "965": case "967": case "968": case "969": case "970": case "971": case "972": case "973": case "974": case "975": case "976": case "977": case "978": case "979": case "980": case "981": case "982": case "983": case "984": case "985": case "986": case "987": case "988": case "989": case "990": case "991": case "992": case "993": case "994": case "995": case "996": case "997": case "998": case "1000": case "1001": case "1002": case "1003": case "1004": case "1005": case "1006": case "1007": case "1008": case "1009": case "1010": case "1011": case "1012": case "1013": case "1014": case "1015": case "1016": case "1017": case "1018": case "1019": case "1020": case "1021": case "1022": case "1023": case "1024": case "1026": case "1028": case "1029": case "1032": case "1033": case "1034": case "1035": case "1036": case "1037": case "1038": case "1039": case "1040": case "1041": case "1042": case "1043": case "1044": case "1045": case "1046": case "1047": case "1048": case "1049": case "1050": case "1051": case "1052": case "1053": case "1054": case "1055": case "1056": case "1057": case "1058": case "1059": case "1060": case "1061": case "1062": case "1063": case "1064": case "1065": case "1066": case "1067": case "1068": case "1069": case "1070": case "1071": case "1072": case "1073": case "1074": case "1075": case "1076": case "1077": case "1078": case "1079": case "1080": case "1081": case "1082": case "1083": case "1084": case "1085": case "1086": case "1087": case "1088": case "1089": case "1090": case "1091": case "1092": case "1093": case "1095": case "1096": case "1097": case "1098": case "1099": case "1100": case "1101": case "1102": case "1103": case "1104": case "1105": case "1106": case "1107": case "1108": case "1109": case "1110": case "1111": case "1112": case "1113": case "1114": case "1115": case "1116": case "1117": case "1118": case "1119": case "1120": case "1121": case "1122": case "1123": case "1124": case "1125": case "1126": case "1127": case "1128": case "1129": case "1131": case "1132": case "1133": case "1134": case "1137": case "1138": case "1139": case "1140": case "1141": case "1143": case "1144": case "1145": case "1150": case "1151": case "1152": case "1153": case "1154": case "1156": case "1160": case "1164": case "1166": case "1167": case "1168": case "1169": case "1171": case "1174": case "1180": case "1182": case "1185": case "1188": case "1190": case "1191": case "1192": case "1193": case "1195": case "1196": case "1197": case "1198": case "1200": case "1201": case "1204": case "1205": case "1206": case "1208": case "1209": case "1211": case "1212": case "1213": case "1214": case "1215": case "1220": case "1221": case "1222": case "1227": case "1229": case "1230": case "1231": case "1232": case "1237": case "1238": 
                    return {"color": "#111827", "fillColor": "#f7fbff", "fillOpacity": 0.8, "opacity": 1.0, "weight": 2.0};
                case "11": case "12": case "395": case "1203": case "1219": 
                    return {"color": "#111827", "fillColor": "#fc8d59", "fillOpacity": 0.8, "opacity": 1.0, "weight": 2.0};
                case "20": case "166": case "192": case "481": case "697": case "713": case "725": case "786": case "788": case "808": case "844": case "871": case "912": case "913": case "1155": case "1157": case "1158": case "1161": case "1175": case "1176": case "1177": case "1181": case "1187": case "1216": 
                    return {"color": "#111827", "fillColor": "#fdbb84", "fillOpacity": 0.8, "opacity": 1.0, "weight": 2.0};
                default:
                    return {"color": "#111827", "fillColor": "#fee8c8", "fillOpacity": 0.8, "opacity": 1.0, "weight": 2.0};
            }
        }

        function geo_json_3171758a9cc9684c2da02e0a1928d3e0_onEachFeature(feature, layer) {

            layer.on({
                mouseout: function(e) {
                    if(typeof e.target.setStyle === "function"){
                            geo_json_3171758a9cc9684c2da02e0a1928d3e0.resetStyle(e.target);
                    }
                },
                mouseover: function(e) {
                    if(typeof e.target.setStyle === "function"){
                        const highlightStyle = geo_json_3171758a9cc9684c2da02e0a1928d3e0_highlighter(e.target.feature)
                        e.target.setStyle(highlightStyle);
                    }
                },
            });
        };
        var geo_json_3171758a9cc9684c2da02e0a1928d3e0 = L.geoJson(null, {
                onEachFeature: geo_json_3171758a9cc9684c2da02e0a1928d3e0_onEachFeature,
            
                style: geo_json_3171758a9cc9684c2da02e0a1928d3e0_styler,
            ...{
}
        });

        function geo_json_3171758a9cc9684c2da02e0a1928d3e0_add (data) {
            geo_json_3171758a9cc9684c2da02e0a1928d3e0
                .addData(data);
        }
            /* Exact geometry and attributes loaded on demand. */

        
    
    geo_json_3171758a9cc9684c2da02e0a1928d3e0.bindTooltip(
    function(layer){
    let div = L.DomUtil.create('div');
    
    let handleObject = feature => {
        if (feature === null) {
            return '';
        } else if (typeof(feature)=='object') {
            return JSON.stringify(feature);
        } else {
            return feature;
        }
    }
    let fields = ["GEOID20", "COUNTY_NAME", "PERCENT_WUI", "EST_ACS_POP_EXPOSED", "EST_ACS_HOUSING_EXPOSED"];
    let aliases = ["Block Group GEOID:", "County:", "WUI Exposure (%):", "Estimated Exposed Population in Block Group:", "Estimated Housing Units Exposed:"];
    let table = '<table>' +
        String(
        fields.map(
        (v,i)=>
        `<tr>
            <th>${aliases[i].toLocaleString()}</th>
            
            <td>${handleObject(layer.feature.properties[v]).toLocaleString()}</td>
        </tr>`).join(''))
    +'</table>';
    div.innerHTML=table;
    
    return div
    }
    ,{
  "sticky": false,
  "className": "foliumtooltip",
});
                     
    
    geo_json_3171758a9cc9684c2da02e0a1928d3e0.bindPopup(
    function(layer){
    let div = L.DomUtil.create('div');
    
    let handleObject = feature => {
        if (feature === null) {
            return '';
        } else if (typeof(feature)=='object') {
            return JSON.stringify(feature);
        } else {
            return feature;
        }
    }
    let fields = ["GEOID20", "COUNTY_NAME", "EXPOSURE_STATUS", "WUI_EXPOSURE_CLASS", "ACS_POPULATION", "ACS_HOUSING_UNITS", "BLOCK_GROUP_AREA_KM2", "EXPOSED_AREA_KM2", "PERCENT_WUI", "EST_ACS_POP_EXPOSED", "EST_ACS_HOUSING_EXPOSED", "INTERSECTING_WUI_POLYGONS"];
    let aliases = ["Block Group GEOID:", "County:", "Exposure Status:", "Exposure Class:", "ACS Population Estimate:", "ACS Housing Unit Estimate:", "Block Group Area (km\u00b2):", "WUI-Exposed Area (km\u00b2):", "Percent Inside WUI:", "Estimated Exposed Population in Block Group:", "Estimated Housing Units Exposed:", "Intersecting WUI Polygons:"];
    let table = '<table>' +
        String(
        fields.map(
        (v,i)=>
        `<tr>
            <th>${aliases[i].toLocaleString()}</th>
            
            <td>${handleObject(layer.feature.properties[v]).toLocaleString()}</td>
        </tr>`).join(''))
    +'</table>';
    div.innerHTML=table;
    
    return div
    }
    ,{
  "className": "foliumpopup",
});
                     
    
            geo_json_3171758a9cc9684c2da02e0a1928d3e0.addTo(feature_group_738a8bd9e920586fc11716d9f694f329);
        
    
            
        
    
            var feature_group_6e5997ea896523cfbcdea3ba156cbb40 = L.featureGroup();
        
    
            var feature_group_1888bcf1ed8ac1a8b073ea29d258b507 = L.featureGroup();
        
    
            var feature_group_e1939e12a90595de638272f196a18b9f = L.featureGroup();
        
    
            var feature_group_98011f5b58e92644ffbb1fed95305760 = L.featureGroup();
        
    
            var feature_group_da6cd3e985b966b45a91e38fea5303b7 = L.featureGroup();
        
    

    // Reference the Leaflet map created by Folium.
    var dashboardMap = map_d1b7ce120271f28f3680a3a773fb74bb;

    // Retrieve the HTML element containing the map.
    var dashboardMapContainer = (
        dashboardMap.getContainer()
    );

    // ------------------------------------------------
    // CREATE CUSTOM FULLSCREEN CONTROL
    // ------------------------------------------------

    // Create a Leaflet control positioned below the standard zoom controls.
    var DashboardFullscreenControl = L.Control.extend({

        options: {
            position: "topleft"
        },

        onAdd: function(map) {

            // Create the fullscreen control container.
            var fullscreenContainer = L.DomUtil.create(
                "div",
                "dashboard-fullscreen-control"
            );

            // Create the clickable fullscreen button.
            var fullscreenButton = L.DomUtil.create(
                "a",
                "dashboard-fullscreen-button",
                fullscreenContainer
            );

            // Display a simple expand symbol.
            fullscreenButton.innerHTML = "⛶";

            // Add accessible button information.
            fullscreenButton.href = "#";
            fullscreenButton.title = "Open Fullscreen";
            fullscreenButton.setAttribute(
                "aria-label",
                "Open fullscreen map"
            );

            // Prevent map movement when the control itself is clicked.
            L.DomEvent.disableClickPropagation(
                fullscreenContainer
            );

            L.DomEvent.disableScrollPropagation(
                fullscreenContainer
            );

            // Enter or exit browser fullscreen mode when the button is clicked.
            L.DomEvent.on(
                fullscreenButton,
                "click",
                function(event) {

                    L.DomEvent.preventDefault(event);
                    L.DomEvent.stopPropagation(event);

                    // Determine whether the browser is currently displaying
                    // a fullscreen element.
                    var fullscreenElement = (
                        document.fullscreenElement
                        || document.webkitFullscreenElement
                        || document.mozFullScreenElement
                        || document.msFullscreenElement
                    );

                    var wuiFullscreenTarget = document.getElementById('wui-app') || dashboardMapContainer;
                    if (!fullscreenElement) {

                        // Request fullscreen mode using the method supported by the browser.
                        if (wuiFullscreenTarget.requestFullscreen) {
                            wuiFullscreenTarget.requestFullscreen();
                        } else if (wuiFullscreenTarget.webkitRequestFullscreen) {
                            wuiFullscreenTarget.webkitRequestFullscreen();
                        } else if (wuiFullscreenTarget.mozRequestFullScreen) {
                            wuiFullscreenTarget.mozRequestFullScreen();
                        } else if (wuiFullscreenTarget.msRequestFullscreen) {
                            wuiFullscreenTarget.msRequestFullscreen();
                        }

                    } else {

                        // Exit fullscreen mode using the method supported by the browser.
                        if (document.exitFullscreen) {
                            document.exitFullscreen();
                        } else if (document.webkitExitFullscreen) {
                            document.webkitExitFullscreen();
                        } else if (document.mozCancelFullScreen) {
                            document.mozCancelFullScreen();
                        } else if (document.msExitFullscreen) {
                            document.msExitFullscreen();
                        }
                    }
                }
            );

            return fullscreenContainer;
        }
    });

    // Add the completed fullscreen control to the map.
    dashboardMap.addControl(
        new DashboardFullscreenControl()
    );

    // ------------------------------------------------
    // CREATE RESET-VIEW CONTROL
    // ------------------------------------------------

    // Preserve the original fitted extent used when the dashboard first opens.
    var dashboardResetViewBounds = L.latLngBounds(
        [[36.999962312497104, -114.052896913423], [40.92186613448939, -110.85765798208]]
    );

    // Create a Leaflet control positioned with the other navigation controls.
    var DashboardResetViewControl = L.Control.extend({

        options: {
            position: "topleft"
        },

        onAdd: function(map) {

            // Create the reset-view control container.
            var resetViewContainer = L.DomUtil.create(
                "div",
                "dashboard-reset-view-control"
            );

            // Create the clickable reset-view button.
            var resetViewButton = L.DomUtil.create(
                "a",
                "dashboard-reset-view-button",
                resetViewContainer
            );

            // Display a familiar home symbol for the original map extent.
            resetViewButton.innerHTML = "⌂";
            resetViewButton.href = "#";
            resetViewButton.title = "Reset Map View";
            resetViewButton.setAttribute(
                "aria-label",
                "Reset map to the three-county study area"
            );

            // Prevent the control from triggering map drag or zoom behavior.
            L.DomEvent.disableClickPropagation(
                resetViewContainer
            );

            L.DomEvent.disableScrollPropagation(
                resetViewContainer
            );

            // Restore the original three-county extent when the button is clicked.
            L.DomEvent.on(
                resetViewButton,
                "click",
                function(event) {
                    L.DomEvent.preventDefault(event);
                    L.DomEvent.stopPropagation(event);

                    dashboardMap.fitBounds(
                        dashboardResetViewBounds,
                        {
                            paddingTopLeft: [20, 20],
                            paddingBottomRight: [20, 20]
                        }
                    );
                }
            );

            return resetViewContainer;
        }
    });

    // Add the reset-view control beneath the existing upper-left controls.
    dashboardMap.addControl(
        new DashboardResetViewControl()
    );

    // ------------------------------------------------
    // UPDATE MAP AFTER FULLSCREEN CHANGES
    // ------------------------------------------------

    // Resize the Leaflet map after entering or leaving fullscreen mode so
    // tiles and overlays render correctly.
    function updateDashboardMapSize() {
        window.setTimeout(
            function() {
                dashboardMap.invalidateSize();
            },
            200
        );
    }

    // Listen for standard and browser-specific fullscreen change events.
    document.addEventListener("fullscreenchange", updateDashboardMapSize);
    document.addEventListener("webkitfullscreenchange", updateDashboardMapSize);
    document.addEventListener("mozfullscreenchange", updateDashboardMapSize);
    document.addEventListener("MSFullscreenChange", updateDashboardMapSize);

    // ------------------------------------------------
    // CREATE CUSTOM MOUSE POSITION CONTROL
    // ------------------------------------------------

    // Create a Leaflet control for displaying live latitude and longitude values.
    var DashboardMousePositionControl = L.Control.extend({

        options: {
            position: "bottomright"
        },

        onAdd: function(map) {
            this._container = L.DomUtil.create(
                "div",
                "dashboard-mouse-position"
            );
            this._container.innerHTML = (
                "Latitude: -- | Longitude: --"
            );
            L.DomEvent.disableClickPropagation(this._container);
            return this._container;
        }
    });

    // Create and add the mouse-position control object.
    var dashboardMousePositionControl = (
        new DashboardMousePositionControl()
    );

    dashboardMap.addControl(
        dashboardMousePositionControl
    );

    // Update the coordinate display whenever the cursor moves across the map.
    dashboardMap.on("mousemove", function(event) {
        var latitude = event.latlng.lat.toFixed(5);
        var longitude = event.latlng.lng.toFixed(5);
        dashboardMousePositionControl._container.innerHTML = (
            "Latitude: " + latitude + "° | Longitude: " + longitude + "°"
        );
    });

    // Restore placeholder text when the cursor leaves the map display.
    dashboardMap.on("mouseout", function() {
        dashboardMousePositionControl._container.innerHTML = (
            "Latitude: -- | Longitude: --"
        );
    });

    
            var image_overlay_863723ce4817400a3676643818e14004 = L.imageOverlay(
                "assets/hazard.png",
                [[36.97625858609336, -114.22139953896779], [40.92651832981672, -110.8552470430477]],
                {
  "opacity": 0.58,
  "interactive": false,
  "crossOrigin": false,
  "zindex": 1,
}
            );
        
    
            image_overlay_863723ce4817400a3676643818e14004.addTo(map_d1b7ce120271f28f3680a3a773fb74bb);
        
    
(function () {
  'use strict';
  var map = map_d1b7ce120271f28f3680a3a773fb74bb;
  var app = document.getElementById('wui-app');
  var sidebar = document.getElementById('wui-sidebar');
  var stage = document.getElementById('wui-map-stage');
  var toggle = document.getElementById('wui-sidebar-toggle');
  var close = document.getElementById('wui-sidebar-close');
  var mobile = window.matchMedia('(max-width:850px)');
  var layers = {
    'hazard': image_overlay_863723ce4817400a3676643818e14004,
    'wui': feature_group_1d34b2bd2307238c7a702a70b8c84f3c,
    'exposure': feature_group_738a8bd9e920586fc11716d9f694f329,
    'topographic': tile_layer_5e7daf5fa750b39c4fd483a39f11e926,
    'imagery': tile_layer_1edcddab195b6aea4091802000c2bf36,
    'salt-lake': feature_group_08a88c73f1e663f12f9156a14e65f217,
    'utah': feature_group_5dc82d5dc5d86b36554fc9189fd11c3f,
    'washington': feature_group_a5b3848c21960057590945d931e8abac,
    'hospitals': feature_group_6e5997ea896523cfbcdea3ba156cbb40,
    'fire': feature_group_1888bcf1ed8ac1a8b073ea29d258b507,
    'police': feature_group_e1939e12a90595de638272f196a18b9f,
    'schools': feature_group_98011f5b58e92644ffbb1fed95305760,
    'shelters': feature_group_da6cd3e985b966b45a91e38fea5303b7
    
  };
  var basemaps = ['topographic', 'imagery'];
var deferredLayers = {
'salt-lake': {apply: function(data) { geo_json_e219ca67f284451dfe2bb9b0f70b6ed6_add(data); }},
'utah': {apply: function(data) { geo_json_e6cbce1cc23c42f8856060f9c9f015e8_add(data); }},
'washington': {apply: function(data) { geo_json_352e79a818e7f6adb399345209edd260_add(data); }},
'wui': {apply: function(data) { geo_json_c4ce6f29e558d75ea8c8ad5e2241d1ce_add(data); }},
'exposure': {apply: function(data) { geo_json_3171758a9cc9684c2da02e0a1928d3e0_add(data); }},
'hospitals': {apply: function(data) { addFacilities(data, feature_group_6e5997ea896523cfbcdea3ba156cbb40); }},
'fire': {apply: function(data) { addFacilities(data, feature_group_1888bcf1ed8ac1a8b073ea29d258b507); }},
'police': {apply: function(data) { addFacilities(data, feature_group_e1939e12a90595de638272f196a18b9f); }},
'schools': {apply: function(data) { addFacilities(data, feature_group_98011f5b58e92644ffbb1fed95305760); }},
'shelters': {apply: function(data) { addFacilities(data, feature_group_da6cd3e985b966b45a91e38fea5303b7); }}
};
  // Deferred layers keep user intent separate from request and Leaflet state.
  Object.keys(deferredLayers).forEach(function(id) {
    var item = deferredLayers[id];
    item.desired = ['salt-lake','utah','washington'].includes(id);
    item.loaded = false;
    item.pending = null;
    var row = document.getElementById('wui-row-' + id);
    var status = document.createElement('div');
    status.className = 'wui-load-status';
    status.setAttribute('role','status');
    var message = document.createElement('span');
    var retry = document.createElement('button');
    retry.type = 'button'; retry.textContent = 'Retry'; retry.hidden = true;
    retry.setAttribute('aria-label', 'Retry ' + document.getElementById('wui-input-' + id).labels[0].textContent.trim());
    status.append(message,retry); row.append(status);
    item.status = function(text, failed) {
      message.textContent = text; retry.hidden = !failed;
      status.hidden = !text;
      row.setAttribute('aria-busy', String(Boolean(item.pending) && !failed));
    };
    retry.addEventListener('click', function(){selectDeferred(id,true);});
    item.status(item.desired ? 'Loading…' : 'Loads when selected',false);
  });

  function addFacilities(data, group) {
    var cluster = L.markerClusterGroup({disableClusteringAtZoom:13});
    // Construct off-map. Partial layers cannot appear after a failed build.
    data.forEach(function(row) {
      var marker = L.circleMarker(row.position,row.options);
      marker.bindPopup(function(){
        var wrapper = document.createElement('div');
        wrapper.innerHTML = row.popup;
        return wrapper.firstElementChild;
      },{maxWidth:350});
      marker.bindTooltip(row.tooltip,{sticky:false});
      cluster.addLayer(marker);
    });
    group.addLayer(cluster);
  }

  function selectDeferred(id, desired) {
    var item = deferredLayers[id];
    item.desired = desired;
    if (!desired) {
      map.removeLayer(layers[id]);
      item.status(item.loaded ? '' : (item.pending ? 'Loading; hidden when ready' : 'Loads when selected'),false);
      synchronizeSidebar();
      return item.pending || Promise.resolve();
    }
    if (item.loaded) {
      map.addLayer(layers[id]); item.status('',false); synchronizeSidebar();
      return Promise.resolve();
    }
    if (item.pending) {item.status('Loading…',false); synchronizeSidebar(); return item.pending;}
    item.pending = (async function() {
      var controller = new AbortController();
      var timer = setTimeout(function(){controller.abort();},90000);
      var originalChildren = layers[id].getLayers().slice();
      try {
        var response = await fetch('assets/data/' + id + '.json',{signal:controller.signal});
        if (!response.ok) throw new Error('Layer unavailable');
        var data = await response.json();
        item.apply(data);
        item.loaded = true;
        if (item.desired) map.addLayer(layers[id]);
        item.status('',false);
      } catch (error) {
        layers[id].clearLayers();
        originalChildren.forEach(function(child) {
          if(child.clearLayers) child.clearLayers();
          layers[id].addLayer(child);
        });
        map.removeLayer(layers[id]);
        item.desired = false;
        item.status('Could not load this layer. ',true);
      } finally {
        clearTimeout(timer); item.pending = null;
        document.getElementById('wui-row-' + id).setAttribute('aria-busy','false');
        synchronizeSidebar();
      }
    })();
    item.status('Loading…',false); synchronizeSidebar();
    return item.pending;
  }

  var tileStatus = document.getElementById('wui-basemap-status');
  basemaps.forEach(function(id) {
    layers[id].on('tileerror',function(){
      if (map.hasLayer(layers[id])) {
        tileStatus.hidden=false;
        tileStatus.textContent='Some background tiles are unavailable. Data layers remain available. ';
        var retry=document.createElement('button'); retry.type='button'; retry.textContent='Retry basemap';
        retry.onclick=function(){tileStatus.hidden=true; layers[id].redraw();};
        tileStatus.append(retry);
      }
    });
  });

  stage.appendChild(map.getContainer());

  function sidebarIsOpen() { return !app.classList.contains('wui-sidebar-closed'); }
  function setSidebar(open, returnFocus) {
    app.classList.toggle('wui-sidebar-closed', !open);
    sidebar.setAttribute('aria-hidden', String(!open));
    toggle.setAttribute('aria-expanded', String(open));
    toggle.title = open ? 'Hide map sidebar' : 'Show map sidebar';
    // Mobile drawer is modal: map controls must not receive focus behind it.
    stage.inert = mobile.matches && open;
    if (returnFocus) { toggle.focus(); }
    window.requestAnimationFrame(function () { map.invalidateSize({pan:false}); });
  }
  toggle.addEventListener('click', function () {
    var opening = !sidebarIsOpen();
    setSidebar(opening, false);
    if (opening && mobile.matches) { close.focus(); }
  });
  close.addEventListener('click', function () { setSidebar(false, true); });
  document.getElementById('wui-sidebar-backdrop').addEventListener('click', function () { setSidebar(false, true); });
  app.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && sidebarIsOpen()) {
      setSidebar(false, true); event.preventDefault();
    }
    if (event.key === 'Tab' && mobile.matches && sidebarIsOpen()) {
      var focusable = [toggle].concat(Array.from(sidebar.querySelectorAll('button, input, a[href]')))
        .filter(function (el) { return !el.disabled && el.getClientRects().length; });
      var first = focusable[0], last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) { last.focus(); event.preventDefault(); }
      else if (!event.shiftKey && document.activeElement === last) { first.focus(); event.preventDefault(); }
    }
  });
  app.querySelectorAll('.wui-section-toggle, .wui-info').forEach(function (button) {
    button.addEventListener('click', function () {
      var expanded = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', String(!expanded));
      document.getElementById(button.getAttribute('aria-controls')).hidden = expanded;
    });
  });

  function synchronizeSidebar() {
    Object.keys(layers).forEach(function (id) {
      var visible = deferredLayers[id] ? deferredLayers[id].desired : map.hasLayer(layers[id]);
      document.getElementById('wui-input-' + id).checked = visible;
      document.getElementById('wui-row-' + id).classList.toggle('is-active', visible);
      var range = document.getElementById('wui-opacity-' + id);
      if (range) { range.disabled = !visible; }
    });
    app.querySelectorAll('[data-legend-layer]').forEach(function (key) {
      key.hidden = !map.hasLayer(layers[key.dataset.legendLayer]);
    });
    ['wui-facility-key', 'wui-county-key'].forEach(function (id) {
      var group = document.getElementById(id);
      group.hidden = !Array.from(group.querySelectorAll('[data-legend-layer]')).some(function (key) { return !key.hidden; });
    });
    document.getElementById('wui-empty-legend').hidden = Object.keys(layers).some(function (id) {
      return basemaps.indexOf(id) === -1 && map.hasLayer(layers[id]);
    });
  }
  app.querySelectorAll('[data-layer-id]').forEach(function (input) {
    input.addEventListener('change', function () {
      var id = input.dataset.layerId;
      // Capture the input state before layer events synchronize the controls.
      var checked = input.checked;
      if (basemaps.indexOf(id) !== -1) {
        basemaps.forEach(function (other) { if (other !== id) { map.removeLayer(layers[other]); } });
        map.addLayer(layers[id]);
        layers[id].bringToBack();
        map.fire('baselayerchange', {layer:layers[id], name:input.parentElement.textContent.trim()});
      } else {
        if (deferredLayers[id]) { selectDeferred(id, checked); }
        else { if (checked) { map.addLayer(layers[id]); } else { map.removeLayer(layers[id]); }
          map.fire(checked ? 'overlayadd' : 'overlayremove', {layer:layers[id]}); }
      }
      synchronizeSidebar();
    });
  });
  app.querySelectorAll('[data-opacity-id]').forEach(function (range) {
    range.addEventListener('input', function () {
      layers[range.dataset.opacityId].setOpacity(Number(range.value) / 100);
      document.getElementById('wui-opacity-value-' + range.dataset.opacityId).value = range.value + '%';
    });
  });
  // Responsive popup layout v2: preserve an open feature across layout changes.
  var activePopup = null;
  var popupLayoutTimer = null;
  function fitActivePopup() {
    if (!activePopup || !map.hasLayer(activePopup)) { return; }
    var size = map.getSize();
    // Reserve space for content margins, the pointer, map controls, and attribution.
    var width = Math.max(96, Math.min(350, size.x - 112));
    activePopup.options.minWidth = Math.min(300, width);
    activePopup.options.maxWidth = width;
    activePopup.options.maxHeight = Math.max(56, Math.min(450, size.y - 96));
    activePopup.options.autoPan = true;
    activePopup.options.autoPanPaddingTopLeft = L.point(56, 12);
    activePopup.options.autoPanPaddingBottomRight = L.point(10, 32);
    var content = activePopup.getElement().querySelector('.leaflet-popup-content');
    if (content) {
      content.tabIndex = 0;
      content.setAttribute('role', 'region');
      content.setAttribute('aria-label', 'Map feature details');
      L.DomEvent.disableScrollPropagation(content);
    }
    // Re-measure content and let Leaflet pan the complete popup into the map.
    map.stop();
    activePopup.update();
  }
  function schedulePopupLayout() {
    window.clearTimeout(popupLayoutTimer);
    popupLayoutTimer = window.setTimeout(fitActivePopup, 240);
  }
  map.on('popupopen', function (event) {
    activePopup = event.popup;
    schedulePopupLayout();
  });
  map.on('popupclose', function (event) {
    if (activePopup === event.popup) { activePopup = null; }
    window.clearTimeout(popupLayoutTimer);
  });
  map.on('resize', schedulePopupLayout);
  window.addEventListener('resize', schedulePopupLayout);
  window.addEventListener('orientationchange', schedulePopupLayout);
  ['fullscreenchange', 'webkitfullscreenchange', 'mozfullscreenchange', 'MSFullscreenChange']
    .forEach(function (name) { document.addEventListener(name, schedulePopupLayout); });
  map.on('layeradd layerremove', synchronizeSidebar);
  function responsiveLayout() { setSidebar(!mobile.matches, sidebar.contains(document.activeElement)); }
  if (mobile.addEventListener) { mobile.addEventListener('change', responsiveLayout); }
  else { mobile.addListener(responsiveLayout); }
  window.addEventListener('orientationchange', function () {
    window.setTimeout(function () { if (mobile.matches) { setSidebar(false, true); } map.invalidateSize({pan:false}); }, 100);
  });
  if (window.ResizeObserver) {
    new ResizeObserver(function () { map.invalidateSize({pan:false}); }).observe(stage);
  }
  synchronizeSidebar();
  app.querySelectorAll('[data-layer-id]').forEach(function(input){input.disabled=false;});
  Promise.all(['salt-lake','utah','washington'].map(function(id){return selectDeferred(id,true);})).then(function(){window.dispatchEvent(new Event('wui-ready'));});
  setSidebar(!mobile.matches, false);
  window.requestAnimationFrame(function () {
    map.invalidateSize({pan:false});
    map.fitBounds([[36.999962312497104, -114.052896913423], [40.92186613448939, -110.85765798208]], {padding:[24,24]});
  });
})();
