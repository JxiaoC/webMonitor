var hexcase = 0;  /* hex output format. 0 - lowercase; 1 - uppercase        */
var b64pad = ""; /* base-64 pad character. "=" for strict RFC compliance   */
var chrsz = 8;  /* bits per input character. 8 - ASCII; 16 - Unicode      */
let lmd5 = {}

/*
 * Perform a simple self-test to see if the VM is working
 */
function md5_vm_test() {
    return hex_md5("111111") == "96e79218965eb72c92a549dd5a330112";
}

/*
 * Calculate the MD5 of an array of little-endian words, and a bit length
 */
function core_md5(x, len) {
    /* append padding */
    x[len >> 5] |= 0x80 << ((len) % 32);
    x[(((len + 64) >>> 9) << 4) + 14] = len;

    var a = 1732584193;
    var b = -271733879;
    var c = -1732584194;
    var d = 271733878;

    for (var i = 0; i < x.length; i += 16) {
        var olda = a;
        var oldb = b;
        var oldc = c;
        var oldd = d;

        a = md5_ff(a, b, c, d, x[i + 0], 7, -680876936);
        d = md5_ff(d, a, b, c, x[i + 1], 12, -389564586);
        c = md5_ff(c, d, a, b, x[i + 2], 17, 606105819);
        b = md5_ff(b, c, d, a, x[i + 3], 22, -1044525330);
        a = md5_ff(a, b, c, d, x[i + 4], 7, -176418897);
        d = md5_ff(d, a, b, c, x[i + 5], 12, 1200080426);
        c = md5_ff(c, d, a, b, x[i + 6], 17, -1473231341);
        b = md5_ff(b, c, d, a, x[i + 7], 22, -45705983);
        a = md5_ff(a, b, c, d, x[i + 8], 7, 1770035416);
        d = md5_ff(d, a, b, c, x[i + 9], 12, -1958414417);
        c = md5_ff(c, d, a, b, x[i + 10], 17, -42063);
        b = md5_ff(b, c, d, a, x[i + 11], 22, -1990404162);
        a = md5_ff(a, b, c, d, x[i + 12], 7, 1804603682);
        d = md5_ff(d, a, b, c, x[i + 13], 12, -40341101);
        c = md5_ff(c, d, a, b, x[i + 14], 17, -1502002290);
        b = md5_ff(b, c, d, a, x[i + 15], 22, 1236535329);

        a = md5_gg(a, b, c, d, x[i + 1], 5, -165796510);
        d = md5_gg(d, a, b, c, x[i + 6], 9, -1069501632);
        c = md5_gg(c, d, a, b, x[i + 11], 14, 643717713);
        b = md5_gg(b, c, d, a, x[i + 0], 20, -373897302);
        a = md5_gg(a, b, c, d, x[i + 5], 5, -701558691);
        d = md5_gg(d, a, b, c, x[i + 10], 9, 38016083);
        c = md5_gg(c, d, a, b, x[i + 15], 14, -660478335);
        b = md5_gg(b, c, d, a, x[i + 4], 20, -405537848);
        a = md5_gg(a, b, c, d, x[i + 9], 5, 568446438);
        d = md5_gg(d, a, b, c, x[i + 14], 9, -1019803690);
        c = md5_gg(c, d, a, b, x[i + 3], 14, -187363961);
        b = md5_gg(b, c, d, a, x[i + 8], 20, 1163531501);
        a = md5_gg(a, b, c, d, x[i + 13], 5, -1444681467);
        d = md5_gg(d, a, b, c, x[i + 2], 9, -51403784);
        c = md5_gg(c, d, a, b, x[i + 7], 14, 1735328473);
        b = md5_gg(b, c, d, a, x[i + 12], 20, -1926607734);

        a = md5_hh(a, b, c, d, x[i + 5], 4, -378558);
        d = md5_hh(d, a, b, c, x[i + 8], 11, -2022574463);
        c = md5_hh(c, d, a, b, x[i + 11], 16, 1839030562);
        b = md5_hh(b, c, d, a, x[i + 14], 23, -35309556);
        a = md5_hh(a, b, c, d, x[i + 1], 4, -1530992060);
        d = md5_hh(d, a, b, c, x[i + 4], 11, 1272893353);
        c = md5_hh(c, d, a, b, x[i + 7], 16, -155497632);
        b = md5_hh(b, c, d, a, x[i + 10], 23, -1094730640);
        a = md5_hh(a, b, c, d, x[i + 13], 4, 681279174);
        d = md5_hh(d, a, b, c, x[i + 0], 11, -358537222);
        c = md5_hh(c, d, a, b, x[i + 3], 16, -722521979);
        b = md5_hh(b, c, d, a, x[i + 6], 23, 76029189);
        a = md5_hh(a, b, c, d, x[i + 9], 4, -640364487);
        d = md5_hh(d, a, b, c, x[i + 12], 11, -421815835);
        c = md5_hh(c, d, a, b, x[i + 15], 16, 530742520);
        b = md5_hh(b, c, d, a, x[i + 2], 23, -995338651);

        a = md5_ii(a, b, c, d, x[i + 0], 6, -198630844);
        d = md5_ii(d, a, b, c, x[i + 7], 10, 1126891415);
        c = md5_ii(c, d, a, b, x[i + 14], 15, -1416354905);
        b = md5_ii(b, c, d, a, x[i + 5], 21, -57434055);
        a = md5_ii(a, b, c, d, x[i + 12], 6, 1700485571);
        d = md5_ii(d, a, b, c, x[i + 3], 10, -1894986606);
        c = md5_ii(c, d, a, b, x[i + 10], 15, -1051523);
        b = md5_ii(b, c, d, a, x[i + 1], 21, -2054922799);
        a = md5_ii(a, b, c, d, x[i + 8], 6, 1873313359);
        d = md5_ii(d, a, b, c, x[i + 15], 10, -30611744);
        c = md5_ii(c, d, a, b, x[i + 6], 15, -1560198380);
        b = md5_ii(b, c, d, a, x[i + 13], 21, 1309151649);
        a = md5_ii(a, b, c, d, x[i + 4], 6, -145523070);
        d = md5_ii(d, a, b, c, x[i + 11], 10, -1120210379);
        c = md5_ii(c, d, a, b, x[i + 2], 15, 718787259);
        b = md5_ii(b, c, d, a, x[i + 9], 21, -343485551);

        a = safe_add(a, olda);
        b = safe_add(b, oldb);
        c = safe_add(c, oldc);
        d = safe_add(d, oldd);
    }
    return Array(a, b, c, d);

}

/*
 * These functions implement the four basic operations the algorithm uses.
 */
function md5_cmn(q, a, b, x, s, t) {
    return safe_add(bit_rol(safe_add(safe_add(a, q), safe_add(x, t)), s), b);
}
function md5_ff(a, b, c, d, x, s, t) {
    return md5_cmn((b & c) | ((~b) & d), a, b, x, s, t);
}
function md5_gg(a, b, c, d, x, s, t) {
    return md5_cmn((b & d) | (c & (~d)), a, b, x, s, t);
}
function md5_hh(a, b, c, d, x, s, t) {
    return md5_cmn(b ^ c ^ d, a, b, x, s, t);
}
function md5_ii(a, b, c, d, x, s, t) {
    return md5_cmn(c ^ (b | (~d)), a, b, x, s, t);
}

/*
 * Calculate the HMAC-MD5, of a key and some data
 */
function core_hmac_md5(key, data) {
    var bkey = str2binl(key);
    if (bkey.length > 16) bkey = core_md5(bkey, key.length * chrsz);

    var ipad = Array(16), opad = Array(16);
    for (var i = 0; i < 16; i++) {
        ipad[i] = bkey[i] ^ 0x36363636;
        opad[i] = bkey[i] ^ 0x5C5C5C5C;
    }

    var hash = core_md5(ipad.concat(str2binl(data)), 512 + data.length * chrsz);
    return core_md5(opad.concat(hash), 512 + 128);
}

/*
 * Add integers, wrapping at 2^32. This uses 16-bit operations internally
 * to work around bugs in some JS interpreters.
 */
function safe_add(x, y) {
    var lsw = (x & 0xFFFF) + (y & 0xFFFF);
    var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
    return (msw << 16) | (lsw & 0xFFFF);
}

/*
 * Bitwise rotate a 32-bit number to the left.
 */
function bit_rol(num, cnt) {
    return (num << cnt) | (num >>> (32 - cnt));
}

/*
 * Convert a string to an array of little-endian words
 * If chrsz is ASCII, characters >255 have their hi-byte silently ignored.
 */
function str2binl(str) {
    var bin = Array();
    var mask = (1 << chrsz) - 1;
    for (var i = 0; i < str.length * chrsz; i += chrsz)
        bin[i >> 5] |= (str.charCodeAt(i / chrsz) & mask) << (i % 32);
    return bin;
}

/*
 * Convert an array of little-endian words to a string
 */
function binl2str(bin) {
    var str = "";
    var mask = (1 << chrsz) - 1;
    for (var i = 0; i < bin.length * 32; i += chrsz)
        str += String.fromCharCode((bin[i >> 5] >>> (i % 32)) & mask);
    return str;
}

/*
 * Convert an array of little-endian words to a hex string.
 */
function binl2hex(binarray) {
    var hex_tab = hexcase ? "0123456789ABCDEF" : "0123456789abcdef";
    var str = "";
    for (var i = 0; i < binarray.length * 4; i++) {
        str += hex_tab.charAt((binarray[i >> 2] >> ((i % 4) * 8 + 4)) & 0xF) +
            hex_tab.charAt((binarray[i >> 2] >> ((i % 4) * 8)) & 0xF);
    }
    return str;
}

/*
 * Convert an array of little-endian words to a base-64 string
 */
function binl2b64(binarray) {
    var tab = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    var str = "";
    for (var i = 0; i < binarray.length * 4; i += 3) {
        var triplet = (((binarray[i >> 2] >> 8 * (i % 4)) & 0xFF) << 16)
            | (((binarray[i + 1 >> 2] >> 8 * ((i + 1) % 4)) & 0xFF) << 8)
            | ((binarray[i + 2 >> 2] >> 8 * ((i + 2) % 4)) & 0xFF);
        for (var j = 0; j < 4; j++) {
            if (i * 8 + j * 6 > binarray.length * 32) str += b64pad;
            else str += tab.charAt((triplet >> 6 * (3 - j)) & 0x3F);
        }
    }
    return str;
}


/*
 * These are the functions you'll usually want to call
 * They take string arguments and return either hex or base-64 encoded strings
 */
lmd5.hex_md5 = function (s) { return binl2hex(core_md5(str2binl(s), s.length * chrsz)); }
lmd5.b64_md5 = function (s) { return binl2b64(core_md5(str2binl(s), s.length * chrsz)); }
lmd5.str_md5 = function (s) { return binl2str(core_md5(str2binl(s), s.length * chrsz)); }
lmd5.hex_hmac_md5 = function (key, data) { return binl2hex(core_hmac_md5(key, data)); }
lmd5.b64_hmac_md5 = function (key, data) { return binl2b64(core_hmac_md5(key, data)); }
lmd5.str_hmac_md5 = function (key, data) { return binl2str(core_hmac_md5(key, data)); }

var version_='jsjiami.com.v7',_0x1a82=(function(){return[...[version_,'QTjXsGbKjbihpaEmtCiXkW.cbUwoDfmK.urMvV7C==','W4ldUmk+kmkgka','aCkIxW8NWQxdOZ1llaCs','WOdcM3zmwSogW6b4','WQ8qcqGOdcKh','vYNcQmkrvXXTWQldPXNdHCopW6i','uuGpWRpdS8k8','B17dLhuoWRG'],...(function(){return[...['DSo3jM7cTSoCutVcP2VcOvJcIW','saZcSJldJmomyNnOtbmH','WPZcPCoMFmoecIurW5P1W64','W7eyFfVcOgddH8kvv01ssmkz','iN7dSLGQ','ittcMX0AdCkpWOK','jSkSCfLsqhxdO8o3W6/cQSkdqW','hv7dTYKdga','W5VcOSo2hblcHSkeWRJdOmo3hmoKkCo3'],...(function(){return['W6DVWOuNsv/dQ8k2','FSkTBJldT8kqcW','DcxcSCowoH0','chRdRsa+','D8o0qSozWO4','oCkadSkcW7iukWtdGvakW4K','W6tdKJHgkvRcH8k4W6JcThFdUXW','WPjfW6bWwZpdJg/dPmoqWP8K'];}())];}())];}());function _0x54df(_0x42d282,_0x2f6961){var _0x1a8258=_0x1a82;return _0x54df=function(_0x54df7e,_0x43e1ac){_0x54df7e=_0x54df7e-0x87;var _0x5ad5da=_0x1a8258[_0x54df7e];if(_0x54df['kirREf']===undefined){var _0xd89187=function(_0x20c0f9){var _0x1ae0ed='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=';var _0x58e6e9='',_0x5470f7='';for(var _0x6a9170=0x0,_0x397efc,_0x243576,_0x2a651c=0x0;_0x243576=_0x20c0f9['charAt'](_0x2a651c++);~_0x243576&&(_0x397efc=_0x6a9170%0x4?_0x397efc*0x40+_0x243576:_0x243576,_0x6a9170++%0x4)?_0x58e6e9+=String['fromCharCode'](0xff&_0x397efc>>(-0x2*_0x6a9170&0x6)):0x0){_0x243576=_0x1ae0ed['indexOf'](_0x243576);}for(var _0x33b57c=0x0,_0x5bf648=_0x58e6e9['length'];_0x33b57c<_0x5bf648;_0x33b57c++){_0x5470f7+='%'+('00'+_0x58e6e9['charCodeAt'](_0x33b57c)['toString'](0x10))['slice'](-0x2);}return decodeURIComponent(_0x5470f7);};var _0xbf838d=function(_0x4ef4c9,_0xd7954c){var _0x2d4ad9=[],_0x2e8448=0x0,_0x1109c5,_0x4687a0='';_0x4ef4c9=_0xd89187(_0x4ef4c9);var _0x526e27;for(_0x526e27=0x0;_0x526e27<0x100;_0x526e27++){_0x2d4ad9[_0x526e27]=_0x526e27;}for(_0x526e27=0x0;_0x526e27<0x100;_0x526e27++){_0x2e8448=(_0x2e8448+_0x2d4ad9[_0x526e27]+_0xd7954c['charCodeAt'](_0x526e27%_0xd7954c['length']))%0x100,_0x1109c5=_0x2d4ad9[_0x526e27],_0x2d4ad9[_0x526e27]=_0x2d4ad9[_0x2e8448],_0x2d4ad9[_0x2e8448]=_0x1109c5;}_0x526e27=0x0,_0x2e8448=0x0;for(var _0x252028=0x0;_0x252028<_0x4ef4c9['length'];_0x252028++){_0x526e27=(_0x526e27+0x1)%0x100,_0x2e8448=(_0x2e8448+_0x2d4ad9[_0x526e27])%0x100,_0x1109c5=_0x2d4ad9[_0x526e27],_0x2d4ad9[_0x526e27]=_0x2d4ad9[_0x2e8448],_0x2d4ad9[_0x2e8448]=_0x1109c5,_0x4687a0+=String['fromCharCode'](_0x4ef4c9['charCodeAt'](_0x252028)^_0x2d4ad9[(_0x2d4ad9[_0x526e27]+_0x2d4ad9[_0x2e8448])%0x100]);}return _0x4687a0;};_0x54df['MNxpHK']=_0xbf838d,_0x42d282=arguments,_0x54df['kirREf']=!![];}var _0x325aa4=_0x1a8258[0x0],_0x4a615e=_0x54df7e+_0x325aa4,_0x240b72=_0x42d282[_0x4a615e];return!_0x240b72?(_0x54df['mVbZKw']===undefined&&(_0x54df['mVbZKw']=!![]),_0x5ad5da=_0x54df['MNxpHK'](_0x5ad5da,_0x43e1ac),_0x42d282[_0x4a615e]=_0x5ad5da):_0x5ad5da=_0x240b72,_0x5ad5da;},_0x54df(_0x42d282,_0x2f6961);}(function(_0x5dadec,_0xd4369a,_0x36e380,_0x5a7b6e,_0x5e673c,_0x13a7b3,_0x4597d4){return _0x5dadec=_0x5dadec>>0x8,_0x13a7b3='hs',_0x4597d4='hs',function(_0xc31875,_0xa38294,_0x1e3e40,_0x3b8b3f,_0x41a88c){var _0x273d6f=_0x54df;_0x3b8b3f='tfi',_0x13a7b3=_0x3b8b3f+_0x13a7b3,_0x41a88c='up',_0x4597d4+=_0x41a88c,_0x13a7b3=_0x1e3e40(_0x13a7b3),_0x4597d4=_0x1e3e40(_0x4597d4),_0x1e3e40=0x0;var _0x267d90=_0xc31875;while(!![]&&--_0x5a7b6e+_0xa38294){try{_0x3b8b3f=parseInt(_0x273d6f(0x96,'f]9w'))/0x1*(parseInt(_0x273d6f(0x99,'eNzW'))/0x2)+-parseInt(_0x273d6f(0x8e,'59g!'))/0x3*(-parseInt(_0x273d6f(0x9d,'h[ho'))/0x4)+-parseInt(_0x273d6f(0x97,'F@rT'))/0x5+parseInt(_0x273d6f(0x8b,'Iigj'))/0x6+-parseInt(_0x273d6f(0x9c,'MWBn'))/0x7+parseInt(_0x273d6f(0x8a,'5Esz'))/0x8*(parseInt(_0x273d6f(0x9e,'4j6r'))/0x9)+-parseInt(_0x273d6f(0x94,'4j6r'))/0xa;}catch(_0x37880e){_0x3b8b3f=_0x1e3e40;}finally{_0x41a88c=_0x267d90[_0x13a7b3]();if(_0x5dadec<=_0x5a7b6e)_0x1e3e40?_0x5e673c?_0x3b8b3f=_0x41a88c:_0x5e673c=_0x41a88c:_0x1e3e40=_0x41a88c;else{if(_0x1e3e40==_0x5e673c['replace'](/[DCuWhVGKEXMQkpTbrUftw=]/g,'')){if(_0x3b8b3f===_0xa38294){_0x267d90['un'+_0x13a7b3](_0x41a88c);break;}_0x267d90[_0x4597d4](_0x41a88c);}}}}}(_0x36e380,_0xd4369a,function(_0x137bb0,_0x3a89dd,_0x584ae0,_0x26eb86,_0x1bd01b,_0x5319ed,_0x1b0dca){return _0x3a89dd='\x73\x70\x6c\x69\x74',_0x137bb0=arguments[0x0],_0x137bb0=_0x137bb0[_0x3a89dd](''),_0x584ae0=`\x72\x65\x76\x65\x72\x73\x65`,_0x137bb0=_0x137bb0[_0x584ae0]('\x76'),_0x26eb86=`\x6a\x6f\x69\x6e`,(0x11ebf6,_0x137bb0[_0x26eb86](''));});}(0xbe00,0xcf31e,_0x1a82,0xc0),_0x1a82)&&(version_=_0x1a82);function whoisToken(_0x40090d,_0x111fe0,_0x21e24b){var _0x33f601=_0x54df,_0x548aa0={'yAtnI':function(_0xea8202,_0x4a97eb){return _0xea8202==_0x4a97eb;},'PlVtW':function(_0x10a14e,_0x24f98f){return _0x10a14e<_0x24f98f;},'pJVyY':function(_0x3d567e,_0x3ebc4c){return _0x3d567e%_0x3ebc4c;}};if(!_0x111fe0)return'';if(_0x548aa0[_0x33f601(0x88,'hi5r')](!_0x111fe0[_0x33f601(0x92,'&Vw]')],0x0))return'';if(!_0x40090d)return'';if(_0x548aa0[_0x33f601(0x89,'5Esz')](_0x40090d[_0x33f601(0x87,'CvsW')],0x0))return'';if(!_0x21e24b)return'';if(_0x548aa0['yAtnI'](_0x21e24b[_0x33f601(0x8d,'f]9w')],0x0))return'';var _0x28187d=Array['from'](_0x21e24b),_0x4df9d7=Array['from'](_0x111fe0['toString']()),_0x6b74c1=[];for(var _0x3ceaab=0x0;_0x548aa0[_0x33f601(0x98,'*0u1')](_0x3ceaab,_0x4df9d7[_0x33f601(0x93,'jVT[')]);_0x3ceaab++){_0x6b74c1[_0x3ceaab]=_0x28187d[_0x548aa0['pJVyY'](parseInt(_0x4df9d7[_0x3ceaab]),_0x28187d[_0x33f601(0x9b,'hi5r')])];}var _0x312b33=lmd5.hex_md5(_0x6b74c1['join']('')+_0x40090d['toString']());return _0x312b33;}var version_ = 'jsjiami.com.v7';


