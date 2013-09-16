<?xml version="1.0" encoding="UTF-8"?>
<tileset name="terrain_atlas" tilewidth="32" tileheight="32">
 <image source="terrain_atlas.png" width="1024" height="1024"/>
 <terraintypes>
  <terrain name="water" tile="391"/>
  <terrain name="grass" tile="118"/>
  <terrain name="stone" tile="115"/>
  <terrain name="stone2" tile="112"/>
  <terrain name="water2" tile="394"/>
  <terrain name="platform" tile="38"/>
 </terraintypes>
 <tile id="5" terrain=",,,5"/>
 <tile id="6" terrain=",,5,5"/>
 <tile id="7" terrain=",,5,"/>
 <tile id="8" terrain=",5,5,5"/>
 <tile id="9" terrain="5,,5,5"/>
 <tile id="16" terrain="3,3,3,"/>
 <tile id="17" terrain="3,3,,3"/>
 <tile id="19" terrain="2,2,2,"/>
 <tile id="20" terrain="2,2,,2"/>
 <tile id="22" terrain="1,1,1,"/>
 <tile id="23" terrain="1,1,,1"/>
 <tile id="37" terrain=",5,,5"/>
 <tile id="38" terrain="5,5,5,5"/>
 <tile id="39" terrain="5,,5,"/>
 <tile id="40" terrain="5,5,,5"/>
 <tile id="41" terrain="5,5,5,"/>
 <tile id="48" terrain="3,,3,3"/>
 <tile id="49" terrain=",3,3,3"/>
 <tile id="51" terrain="2,,2,2"/>
 <tile id="52" terrain=",2,2,2"/>
 <tile id="54" terrain="1,,1,1"/>
 <tile id="55" terrain=",1,1,1"/>
 <tile id="69" terrain=",5,,"/>
 <tile id="70" terrain="5,5,,"/>
 <tile id="71" terrain="5,,,"/>
 <tile id="79" terrain=",,,3"/>
 <tile id="80" terrain=",,3,3"/>
 <tile id="81" terrain=",,3,"/>
 <tile id="82" terrain=",,,2"/>
 <tile id="83" terrain=",,2,2"/>
 <tile id="84" terrain=",,2,"/>
 <tile id="85" terrain=",,,1"/>
 <tile id="86" terrain=",,1,1"/>
 <tile id="87" terrain=",,1,"/>
 <tile id="111" terrain=",3,,3"/>
 <tile id="112" terrain="3,3,3,3"/>
 <tile id="113" terrain="3,,3,"/>
 <tile id="114" terrain=",2,,2"/>
 <tile id="115" terrain="2,2,2,2"/>
 <tile id="116" terrain="2,,2,"/>
 <tile id="117" terrain=",1,,1"/>
 <tile id="118" terrain="1,1,1,1"/>
 <tile id="119" terrain="1,,1,"/>
 <tile id="143" terrain=",3,,"/>
 <tile id="144" terrain="3,3,,"/>
 <tile id="145" terrain="3,,,"/>
 <tile id="146" terrain=",2,,"/>
 <tile id="147" terrain="2,2,,"/>
 <tile id="148" terrain="2,,,"/>
 <tile id="149" terrain=",1,,"/>
 <tile id="150" terrain="1,1,,"/>
 <tile id="151" terrain="1,,,"/>
 <tile id="175" terrain="3,3,3,3"/>
 <tile id="176" terrain="3,3,3,3"/>
 <tile id="177" terrain="3,3,3,3"/>
 <tile id="178" terrain="2,2,2,2"/>
 <tile id="179" terrain="2,2,2,2"/>
 <tile id="180" terrain="2,2,2,2"/>
 <tile id="181" terrain="1,1,1,1"/>
 <tile id="182" terrain="1,1,1,1"/>
 <tile id="183" terrain="1,1,1,1"/>
 <tile id="213" terrain="1,1,1,"/>
 <tile id="214" terrain="1,1,,1"/>
 <tile id="215" terrain="1,1,,1"/>
 <tile id="245" terrain="1,,1,1"/>
 <tile id="246" terrain=",1,1,1"/>
 <tile id="247" terrain=",1,1,1"/>
 <tile id="277" terrain=",,,1"/>
 <tile id="278" terrain=",,1,1"/>
 <tile id="279" terrain=",,1,"/>
 <tile id="295" terrain="0,0,0,1"/>
 <tile id="296" terrain="0,0,1,0"/>
 <tile id="298" terrain="4,4,4,">
  <properties>
   <property name="animation" value="water/water_s_tl.png"/>
   <property name="delay" value="0.3"/>
   <property name="frames_x" value="2"/>
   <property name="frames_y" value="1"/>
  </properties>
 </tile>
 <tile id="299" terrain="4,4,,4">
  <properties>
   <property name="animation" value="water/water_s_tr.png"/>
   <property name="delay" value="0.3"/>
   <property name="frames_x" value="2"/>
   <property name="frames_y" value="1"/>
  </properties>
 </tile>
 <tile id="309" terrain=",1,,1"/>
 <tile id="310" terrain="1,1,1,1"/>
 <tile id="311" terrain="1,,1,"/>
 <tile id="327" terrain="0,1,0,0"/>
 <tile id="328" terrain="1,0,0,0"/>
 <tile id="330" terrain="4,,4,4">
  <properties>
   <property name="animation" value="water/water_s_bl.png"/>
   <property name="delay" value="0.3"/>
   <property name="frames_x" value="2"/>
   <property name="frames_y" value="1"/>
  </properties>
 </tile>
 <tile id="331" terrain=",4,4,4">
  <properties>
   <property name="animation" value="water/water_s_br.png"/>
   <property name="delay" value="0.3"/>
   <property name="frames_x" value="2"/>
   <property name="frames_y" value="1"/>
  </properties>
 </tile>
 <tile id="341" terrain=",1,,"/>
 <tile id="342" terrain="1,1,,"/>
 <tile id="343" terrain="1,,,"/>
 <tile id="358" terrain="1,1,1,0"/>
 <tile id="359" terrain="1,1,0,0"/>
 <tile id="360" terrain="1,1,0,1"/>
 <tile id="361" terrain=",,,4">
  <properties>
   <property name="animation" value="water/water_b_tl.png"/>
   <property name="delay" value="0.3"/>
   <property name="frames_x" value="2"/>
   <property name="frames_y" value="1"/>
  </properties>
 </tile>
 <tile id="362" terrain=",,4,4">
  <properties>
   <property name="animation" value="water/water_b_tm.png"/>
   <property name="delay" value="0.3"/>
   <property name="frames_x" value="2"/>
   <property name="frames_y" value="1"/>
  </properties>
 </tile>
 <tile id="363" terrain=",,4,">
  <properties>
   <property name="animation" value="water/water_b_tr.png"/>
   <property name="delay" value="0.3"/>
   <property name="frames_x" value="2"/>
   <property name="frames_y" value="1"/>
  </properties>
 </tile>
 <tile id="373" terrain="1,1,1,1"/>
 <tile id="374" terrain="1,1,1,1"/>
 <tile id="375" terrain="1,1,1,1"/>
 <tile id="390" terrain="1,0,1,0"/>
 <tile id="391" terrain="0,0,0,0"/>
 <tile id="392" terrain="0,1,0,1"/>
 <tile id="393" terrain=",4,,4">
  <properties>
   <property name="animation" value="water/water_b_l.png"/>
   <property name="delay" value="0.3"/>
   <property name="frames_x" value="2"/>
   <property name="frames_y" value="1"/>
  </properties>
 </tile>
 <tile id="394" terrain="4,4,4,4"/>
 <tile id="395" terrain="4,,4,">
  <properties>
   <property name="animation" value="water/water_b_r.png"/>
   <property name="delay" value="0.3"/>
   <property name="frames_x" value="2"/>
   <property name="frames_y" value="1"/>
  </properties>
 </tile>
 <tile id="422" terrain="1,0,1,1"/>
 <tile id="423" terrain="0,0,1,1"/>
 <tile id="424" terrain="0,1,1,1"/>
 <tile id="425" terrain=",4,,">
  <properties>
   <property name="animation" value="water/water_b_bl.png"/>
   <property name="delay" value="0.3"/>
   <property name="frames_x" value="2"/>
   <property name="frames_y" value="1"/>
  </properties>
 </tile>
 <tile id="426" terrain="4,4,,">
  <properties>
   <property name="animation" value="water/water_b_bm.png"/>
   <property name="delay" value="0.3"/>
   <property name="frames_x" value="2"/>
   <property name="frames_y" value="1"/>
  </properties>
 </tile>
 <tile id="427" terrain="4,,,">
  <properties>
   <property name="animation" value="water/water_b_br.png"/>
   <property name="delay" value="0.3"/>
   <property name="frames_x" value="2"/>
   <property name="frames_y" value="1"/>
  </properties>
 </tile>
 <tile id="454" terrain="0,0,0,0"/>
 <tile id="455" terrain="0,0,0,0"/>
 <tile id="456" terrain="0,0,0,0"/>
 <tile id="703">
  <properties>
   <property name="solid" value="true"/>
  </properties>
 </tile>
 <tile id="735">
  <properties>
   <property name="solid" value="true"/>
  </properties>
 </tile>
</tileset>
<tileset name="dungeon" tilewidth="32" tileheight="32">
 <image source="dungeonex.png" width="320" height="320"/>
 <tile id="9">
  <properties>
   <property name="animation" value="fire.png"/>
   <property name="delay" value="0.1"/>
   <property name="frames_x" value="1"/>
   <property name="frames_y" value="4"/>
  </properties>
 </tile>
 <tile id="19">
  <properties>
   <property name="animation" value="boil.png"/>
   <property name="delay" value="0.1"/>
   <property name="frames_x" value="1"/>
   <property name="frames_y" value="4"/>
  </properties>
 </tile>
</tileset>

