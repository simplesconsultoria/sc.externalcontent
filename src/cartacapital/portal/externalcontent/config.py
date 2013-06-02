# -*- coding: utf-8 -*-

PROJECTNAME = 'cartacapital.portal.externalcontent'

TEMPLATE = '''<script type='text/javascript'>
var googletag = googletag || {};
googletag.cmd = googletag.cmd || [];
(function() {
var gads = document.createElement('script');
gads.async = true;
gads.type = 'text/javascript';
var useSSL = 'https:' == document.location.protocol;
gads.src = (useSSL ? 'https:' : 'http:') +
'//www.googletagservices.com/tag/js/gpt.js';
var node = document.getElementsByTagName('script')[0];
node.parentNode.insertBefore(gads, node);
})();
</script>
<script type='text/javascript'>
var partner = "%s";
var section = ["blogs", "%s"];
googletag.cmd.push(function() {
googletag.defineSlot('/14147850/Parceiros-Cabecalho', [728, 90],
'div-gpt-ad-1370011663251-0').addService(googletag.pubads())
.setTargeting("section", section)
.setTargeting("partner", partner);
googletag.pubads().enableSingleRequest();
googletag.enableServices();
});
</script>
<!-- Parceiros-Cabecalho -->
<div id='div-gpt-ad-1370011663251-0' style='width:728px; height:90px;'>
<script type='text/javascript'>
googletag.cmd.push(function() {
googletag.display('div-gpt-ad-1370011663251-0'); });
</script>
</div>
<script id="barracartacapitaljs" type="text/javascript"
src="http://js.cartacapital.com.br/barra.js"></script>
'''
