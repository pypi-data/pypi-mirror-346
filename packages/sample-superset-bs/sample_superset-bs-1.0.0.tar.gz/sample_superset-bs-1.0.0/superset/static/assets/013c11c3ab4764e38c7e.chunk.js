"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[4570],{2511:(e,t,a)=>{var l,r;a.d(t,{A:()=>l,v:()=>r}),function(e){e.Simple="SIMPLE",e.Sql="SQL"}(l||(l={})),function(e){e.Having="HAVING",e.Where="WHERE"}(r||(r={}))},5815:(e,t,a)=>{a.d(t,{SO:()=>s,Sg:()=>o,pA:()=>n});var l=a(87903),r=a(15151),i=a(2511);const n=(e,t,a=!1,l=!1)=>{const r={};return a?r.adhoc_filters=[{expressionType:i.A.Sql,clause:i.v.Where,sqlExpression:"1 = 0"}]:null!=t&&0!==t.length&&(r.filters=[{col:e,op:l?"NOT IN":"IN",val:t}]),r},s=(e,t,a)=>{const l=[];return null!=t&&t!==a&&l.push({col:e,op:">=",val:t}),null!=a&&a!==t&&l.push({col:e,op:"<=",val:a}),null!=a&&null!=t&&a===t&&l.push({col:e,op:"==",val:a}),l.length?{filters:l}:{}};function o({timeFormatter:e,numberFormatter:t}={}){return(a,i)=>{if(null==a)return r.mu;if("boolean"==typeof a)return a?r.PU:r.qC;if(i===l.s.Boolean)try{return JSON.parse(String(a).toLowerCase())?r.PU:r.qC}catch{return r.qC}return"string"==typeof a?a:"bigint"==typeof a?String(a):e&&i===l.s.Temporal?e(a):t&&"number"==typeof a&&i===l.s.Numeric?t(a):String(a)}}},67874:(e,t,a)=>{a.d(t,{JF:()=>s,Mo:()=>o,YH:()=>i,j3:()=>n});var l=a(96453),r=a(86523);const i=0,n=l.I4.div`
  min-height: ${({height:e})=>e}px;
  width: ${({width:e})=>e===i?"100%":`${e}px`};
`,s=(0,l.I4)(r.A)`
  &.ant-row.ant-form-item {
    margin: 0;
  }
`,o=l.I4.div`
  color: ${({theme:e,status:t="error"})=>{var a;return null==(a=e.colors[t])?void 0:a.base}};
`},84570:(e,t,a)=>{a.r(t),a.d(t,{default:()=>A});var l=a(98023),r=a.n(l),i=a(96453),n=a(32142),s=a(53682),o=a(78518),u=a(62952),d=a(86444),c=a(65482),v=a(96540),m=a(90868),h=a(10504),p=a(2445);const g=i.I4.div`
  display: flex;
  width: 100%;
  position: absolute;
  left: 0;
  top: 100%;
  margin-top: ${({theme:e})=>e.gridUnit}px;
`,f=i.I4.span`
  font-size: ${({theme:e})=>e.typography.sizes.xs}px;
  color: ${({theme:e})=>e.colors.grayscale.light1};
  font-weight: ${({theme:e})=>e.typography.weights.medium};
`,y=({value:e})=>(0,p.Y)(g,{children:(0,p.Y)(f,{children:e})});var b=a(67874),x=a(5815),M=a(23876);const S=i.I4.span`
  margin: 0 ${({theme:e})=>3*e.gridUnit}px;
  color: ${({theme:e})=>e.colors.grayscale.light1};
  font-weight: ${({theme:e})=>e.typography.weights.bold};
  font-size: ${({theme:e})=>e.typography.sizes.m}px;
  align-content: center;
`,$=i.I4.div`
  display: flex;
  justify-content: space-between;

  .antd5-input-number {
    width: 100%;
    position: relative;
  }
`,F=(0,n.gV)(s.A.SMART_NUMBER),w=(e,t,a=!1)=>a&&null!==e||null!==e&&e===t?`x = ${F(e)}`:null!==e&&null!==t?`${F(e)} ≤ x ≤ ${F(t)}`:null!==e?`x ≥ ${F(e)}`:null!==t?`x ≤ ${F(t)}`:"",I=(e,t,a,l,i)=>{const[n,s]=e,u=(0,o.t)("Filter value is required"),d=(0,o.t)("Please provide a value within range");if(void 0!==i){const e=i===M.y.Minimum||i===M.y.Exact?n:s;return!e&&l?{isValid:!1,errorMessage:u}:r()(e)&&(e<t||e>a)?{isValid:!1,errorMessage:d}:{isValid:!0,errorMessage:null}}if(l&&(null===n||null===s))return{isValid:!1,errorMessage:(0,o.t)("Please provide a valid range")};if(!l&&null!==n!=(null!==s))return{isValid:!1,errorMessage:(0,o.t)("Please provide a valid range")};if(null!==n&&null!==s){if(n>s)return{isValid:!1,errorMessage:(0,o.t)("Minimum value cannot be higher than maximum value")};if(n<t||s>a)return{isValid:!1,errorMessage:(0,o.t)("Your range is not within the dataset range")}}return{isValid:!0,errorMessage:null}};function A(e){const{data:t,formData:a,height:l,width:r,setDataMask:i,setFocusedFilter:n,unsetFocusedFilter:s,setHoveredFilter:g,unsetHoveredFilter:f,setFilterActive:F,filterState:A,inputRef:N,filterBarOrientation:V=h.QI.Vertical}=e,[E]=t,{min:Y,max:q}=E,{groupby:C,enableSingleValue:k,enableEmptyFilter:z,defaultValue:D}=a,T=k===M.y.Exact,U=void 0===k,[H=""]=(0,u.A)(C).map(d.A),[O,P]=(0,v.useState)(A.value||D||[null,null]),[B,J]=(0,v.useState)(null),L=(0,v.useCallback)((e=>{i({extraFormData:{},filterState:{value:null,label:"",validateStatus:"error",validateMessage:e||""}})}),[i]),R=(0,v.useCallback)((e=>{const[t,a]=e;i({extraFormData:(0,x.SO)(H,t,a),filterState:{value:T?[t,t]:[t,a],label:w(t,a,T),validateStatus:void 0,validateMessage:""}})}),[i]);(0,v.useEffect)((()=>{if(void 0!==(null==E?void 0:E.min)||void 0!==(null==E?void 0:E.max)){if("error"===A.validateStatus&&B!==A.validateMessage){J(A.validateMessage);const[e,t]=O,{isValid:a,errorMessage:l}=I(O,Y,q,z,k),r=null===e&&null===t&&"error"===A.validateStatus;return!a||r?(J(l),void L(l)):(J(null),void R(O))}if("error"!==A.validateStatus)return void 0!==A.value||A.validateStatus?void((0,c.A)(D,O)?R(D):A.value&&!A.validateStatus&&(P(A.value),R(A.value))):(P([null,null]),void R([null,null]));J(A.validateMessage)}}),[JSON.stringify(A.value)]);const j=(0,v.useMemo)((()=>{switch(k){case M.y.Minimum:return(0,o.t)("Filters for values greater than or equal.");case M.y.Maximum:return(0,o.t)("Filters for values less than or equal.");case M.y.Exact:return(0,o.t)("Filters for values equal to this exact value.");default:return""}}),[k]),Q=(0,v.useCallback)(((e,t)=>{if(void 0===(null==E?void 0:E.min)&&void 0===(null==E?void 0:E.max))return;const a=0===t?[e,O[1]]:[O[0],e];P(a);const{isValid:l,errorMessage:r}=I(a,Y,q,z,k);if(!l)return J(r),void L(r);J(null),R(a)}),[H,Y,q,z,k,i]),W=(0,v.useMemo)((()=>{if(B)return(0,p.Y)(b.Mo,{status:"error",children:B})}),[B]);return(0,v.useEffect)((()=>{switch(k){case M.y.Minimum:case M.y.Exact:Q(null,1);break;case M.y.Maximum:Q(null,0)}i({extraFormData:{},filterState:{value:null,label:""}})}),[k]),(0,p.Y)(b.j3,{height:l,width:r,children:Number.isNaN(Number(Y))||Number.isNaN(Number(q))?(0,p.Y)("h4",{children:(0,o.t)("Chosen non-numeric column")}):(0,p.FD)(b.JF,{"aria-labelledby":`filter-name-${a.nativeFilterId}`,extra:W,children:[(0,p.FD)($,{tabIndex:-1,ref:N,onFocus:n,onBlur:s,onMouseEnter:g,onMouseLeave:f,onMouseDown:()=>F(!0),onMouseUp:()=>F(!1),children:[(k===M.y.Minimum||k===M.y.Exact||void 0===k)&&(0,p.Y)(m.YI,{value:O[0],onChange:e=>Q(e,0),placeholder:`${Y}`,status:A.validateStatus}),void 0===k&&(0,p.Y)(S,{children:"-"}),(k===M.y.Maximum||void 0===k)&&(0,p.Y)(m.YI,{value:O[1],onChange:e=>Q(e,1),placeholder:`${q}`,status:A.validateStatus})]}),(U||V===h.QI.Vertical)&&!A.validateStatus&&(0,p.Y)(y,{value:j})]})})}},86523:(e,t,a)=>{a.d(t,{A:()=>r});var l=a(77925);const r=(0,a(96453).I4)(l.A.Item)`
  ${({theme:e})=>`\n    .ant-form-item-label {\n      padding-bottom: ${e.gridUnit}px;\n      & > label {\n        font-size: ${e.typography.sizes.s}px;\n        color: ${e.colors.grayscale.base};\n\n        &.ant-form-item-required:not(.ant-form-item-required-mark-optional) {\n          &::before {\n            display: none;\n          }\n          &::after {\n            display: inline-block;\n            color: ${e.colors.error.base};\n            font-size: ${e.typography.sizes.s}px;\n            content: '*';\n          }\n        }\n      }\n    }\n  `}
`},90868:(e,t,a)=>{a.d(t,{YI:()=>n,fs:()=>s,pd:()=>i});var l=a(11795),r=a(80566);const i=l.A,n=r.A,{TextArea:s}=l.A}}]);