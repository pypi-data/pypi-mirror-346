"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[1963],{19980:(e,a,t)=>{t.d(a,{A:()=>R});var n=t(96540),l=t(35742),r=t(51436),i=t(78518),o=t(85861),s=t(46920),d=t(75488),c=t(61693),h=t(15595),u=t(67073),p=t(90868),m=t(58561),g=t.n(m),b=t(5261),v=t(40563),f=t(96453),y=t(17437);const _=(0,f.I4)(v.eI)`
  ${({theme:e})=>y.AH`
    flex: 1;
    margin-top: 0;
    margin-bottom: ${2.5*e.gridUnit}px;
  }
  `}
`,x=f.I4.div`
  display: flex;
  align-items: center;
  margin-top: 0;
`,Y=y.AH`
  .antd5-modal-body {
    padding-left: 0;
    padding-right: 0;
    padding-top: 0;
  }
`,w=e=>y.AH`
  .switch-label {
    color: ${e.colors.grayscale.base};
    margin-left: ${4*e.gridUnit}px;
  }
`,C=e=>y.AH`
  .antd5-modal-header {
    padding: ${4.5*e.gridUnit}px ${4*e.gridUnit}px
      ${4*e.gridUnit}px;
  }

  .antd5-modal-close-x .close {
    opacity: 1;
  }

  .antd5-modal-body {
    height: ${180.5*e.gridUnit}px;
  }

  .antd5-modal-footer {
    height: ${16.25*e.gridUnit}px;
  }

  .info-solid-small {
    vertical-align: bottom;
  }
`;var S=t(46740),A=t(2445);const F=f.I4.div`
  //margin-top: 10px;
  //margin-bottom: 10px;
`,D=({columns:e,maxColumnsToShow:a=4})=>{const t=e.map((e=>({name:e})));return(0,A.FD)(F,{children:[(0,A.Y)(h.o5.Text,{type:"secondary",children:"Columns:"}),0===e.length?(0,A.Y)("p",{className:"help-block",children:(0,i.t)("Upload file to preview columns")}):(0,A.Y)(S.A,{tags:t,maxTags:a})]})};var N=t(31641);const E=({label:e,tip:a,children:t,name:n,rules:l})=>(0,A.Y)(_,{label:(0,A.FD)("div",{children:[e,(0,A.Y)(N.A,{tooltip:a})]}),name:n,rules:l,children:t}),k=["delimiter","skip_initial_space","skip_blank_lines","day_first","column_data_types","column_dates","decimal_character","null_values","index_column","header_row","rows_to_read","skip_rows"],$=["sheet_name","column_dates","decimal_character","null_values","index_column","header_row","rows_to_read","skip_rows"],I=[],T=["rows_to_read","index_column"],U=[...k,...$,...I],P={csv:k,excel:$,columnar:I},q=(e,a)=>P[a].includes(e),O={table_name:"",schema:"",sheet_name:void 0,delimiter:",",already_exists:"fail",skip_initial_space:!1,skip_blank_lines:!1,day_first:!1,decimal_character:".",null_values:[],header_row:"0",rows_to_read:null,skip_rows:"0",column_dates:[],index_column:null,dataframe_index:!1,index_label:"",columns_read:[],column_data_types:""},z={csv:".csv, .tsv",excel:".xls, .xlsx",columnar:".parquet, .zip"},M={csv:"CSV",excel:"Excel",columnar:"Columnar"},L=({label:e,dataTest:a,children:t,...n})=>(0,A.FD)(x,{children:[(0,A.Y)(d.d,{...n}),(0,A.Y)("div",{className:"switch-label",children:e}),t]}),R=(0,b.Ay)((({addDangerToast:e,addSuccessToast:a,onHide:t,show:d,allowedExtensions:m,type:b="csv"})=>{const[v]=h.Wq.useForm(),[f,x]=(0,n.useState)(0),[S,F]=(0,n.useState)([]),[N,k]=(0,n.useState)([]),[$,I]=(0,n.useState)([]),[R,H]=(0,n.useState)({}),[j,V]=(0,n.useState)(","),[B,K]=(0,n.useState)(!1),[W,G]=(0,n.useState)(),[Q,J]=(0,n.useState)(!1),[X,Z]=(0,n.useState)(!0),[ee,ae]=(0,n.useState)(!1),te=(0,n.useMemo)((()=>(e="",a,t)=>{const n=g().encode_uri({filters:[{col:"allow_file_upload",opr:"eq",value:!0}],page:a,page_size:t});return l.A.get({endpoint:`/api/v1/database/?q=${n}`}).then((e=>({data:e.json.result.map((e=>({value:e.id,label:e.database_name}))),totalCount:e.json.count})))}),[]),ne=(0,n.useMemo)((()=>(e="",a,t)=>f?l.A.get({endpoint:`/api/v1/database/${f}/schemas/?q=(upload_allowed:!t)`}).then((e=>({data:e.json.result.map((e=>({value:e,label:e}))),totalCount:e.json.count}))):Promise.resolve({data:[],totalCount:0})),[f]),le=a=>{const t=v.getFieldsValue(),n={...O,...t},i=new FormData;return i.append("file",a),"csv"===b&&i.append("delimiter",n.delimiter),i.append("type",b),ae(!0),l.A.post({endpoint:"/api/v1/database/upload_metadata/",body:i,headers:{Accept:"application/json"}}).then((e=>{const{items:a}=e.json.result;if(a&&"excel"!==b)k(a[0].column_names);else{const{allSheetNames:e,sheetColumnNamesMap:t}=a.reduce(((e,a)=>(e.allSheetNames.push(a.sheet_name),e.sheetColumnNamesMap[a.sheet_name]=a.column_names,e)),{allSheetNames:[],sheetColumnNamesMap:{}});k(a[0].column_names),I(e),v.setFieldsValue({sheet_name:e[0]}),H(t)}})).catch((a=>(0,r.h4)(a).then((a=>{e(a.error||"Error"),k([]),v.setFieldsValue({sheet_name:void 0}),I([])})))).finally((()=>{ae(!1)}))},re=()=>{F([]),k([]),G(""),x(0),I([]),K(!1),V(","),Z(!0),ae(!1),H({}),v.resetFields(),t()},ie=()=>N.map((e=>({value:e,label:e})));(0,n.useEffect)((()=>{if(N.length>0&&S[0].originFileObj&&S[0].originFileObj instanceof File){if(!X)return;le(S[0].originFileObj).then((e=>e))}}),[j]);const oe={csv:(0,i.t)("CSV upload"),excel:(0,i.t)("Excel upload"),columnar:(0,i.t)("Columnar upload")};return(0,A.Y)(o.Ay,{css:e=>[Y,C(e),w(e)],primaryButtonLoading:B,name:"database",onHandledPrimaryAction:v.submit,onHide:re,width:"500px",primaryButtonName:"Upload",centered:!0,show:d,title:(0,A.Y)((()=>{const e=oe[b]||(0,i.t)("Upload");return(0,A.Y)("h4",{children:e})}),{}),children:(0,A.Y)(h.Wq,{form:v,onFinish:()=>{var t;const n=v.getFieldsValue();delete n.database,n.schema=W;const o={...O,...n},s=new FormData,d=null==(t=S[0])?void 0:t.originFileObj;d&&s.append("file",d),((e,a)=>{const t=(()=>{const e=P[b]||[];return[...U].filter((a=>!e.includes(a)))})();Object.entries(a).forEach((([a,n])=>{t.includes(a)||T.includes(a)&&null==n||e.append(a,n)}))})(s,o),K(!0);const c=`/api/v1/database/${f}/upload/`;return s.append("type",b),l.A.post({endpoint:c,body:s,headers:{Accept:"application/json"}}).then((()=>{a((0,i.t)("Data imported")),K(!1),re()})).catch((a=>(0,r.h4)(a).then((a=>{e(a.error||"Error")})))).finally((()=>{K(!1)}))},layout:"vertical",initialValues:O,children:(0,A.FD)(c.A,{expandIconPosition:"right",accordion:!0,defaultActiveKey:"general",css:e=>(e=>y.AH`
  .ant-collapse-header {
    padding-top: ${3.5*e.gridUnit}px;
    padding-bottom: ${2.5*e.gridUnit}px;
    .anticon.ant-collapse-arrow {
      top: calc(50% - ${6}px);
    }
    .helper {
      color: ${e.colors.grayscale.base};
      font-size: ${e.typography.sizes.s}px;
    }
  }
  h4 {
    font-size: ${e.typography.sizes.l}px;
    margin-top: 0;
    margin-bottom: ${e.gridUnit}px;
  }
  p.helper {
    margin-bottom: 0;
    padding: 0;
  }
`)(e),children:[(0,A.FD)(c.A.Panel,{header:(0,A.FD)("div",{children:[(0,A.Y)("h4",{children:(0,i.t)("General information")}),(0,A.Y)("p",{className:"helper",children:(0,i.t)("Upload a file to a database.")})]}),children:[(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{label:(0,i.t)("%(label)s file",{label:M[b]}),name:"file",required:!0,rules:[{validator:(e,a)=>0===S.length?Promise.reject((0,i.t)("Uploading a file is required")):((e,a)=>{const t=e.name.match(/.+\.([^.]+)$/);if(!t)return!1;const n=t[1].toLowerCase();return a.map((e=>e.toLowerCase())).includes(n)})(S[0],m)?Promise.resolve():Promise.reject((0,i.t)("Upload a file with a valid extension. Valid: [%s]",m.join(",")))}],children:(0,A.Y)(h._O,{name:"modelFile",id:"modelFile",accept:z[b],fileList:S,onChange:async e=>{F([{...e.file,status:"done"}]),X&&await le(e.file.originFileObj)},onRemove:e=>(F(S.filter((a=>a.uid!==e.uid))),k([]),I([]),v.setFieldsValue({sheet_name:void 0}),!1),customRequest:()=>{},children:(0,A.Y)(s.A,{"aria-label":(0,i.t)("Select"),icon:(0,A.Y)(u.F.UploadOutlined,{}),loading:ee,children:(0,i.t)("Select")})})})})}),(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{children:(0,A.Y)(L,{label:(0,i.t)("Preview uploaded file"),dataTest:"previewUploadedFile",onChange:e=>{Z(e)},checked:X})})})}),X&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(D,{columns:N})})}),(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{label:(0,i.t)("Database"),required:!0,name:"database",rules:[{validator:(e,a)=>f?Promise.resolve():Promise.reject((0,i.t)("Selecting a database is required"))}],children:(0,A.Y)(h.DW,{ariaLabel:(0,i.t)("Select a database"),options:te,onChange:e=>{x(null==e?void 0:e.value),G(void 0),v.setFieldsValue({schema:void 0})},allowClear:!0,placeholder:(0,i.t)("Select a database to upload the file to")})})})}),(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{label:(0,i.t)("Schema"),name:"schema",children:(0,A.Y)(h.DW,{ariaLabel:(0,i.t)("Select a schema"),options:ne,onChange:e=>{G(null==e?void 0:e.value)},allowClear:!0,placeholder:(0,i.t)("Select a schema if the database supports this")})})})}),(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{label:(0,i.t)("Table name"),name:"table_name",required:!0,rules:[{required:!0,message:"Table name is required"}],children:(0,A.Y)(p.pd,{"aria-label":(0,i.t)("Table Name"),name:"table_name",type:"text",placeholder:(0,i.t)("Name of table to be created")})})})}),q("delimiter",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(E,{label:(0,i.t)("Delimiter"),tip:(0,i.t)("Select a delimiter for this data"),name:"delimiter",children:(0,A.Y)(h.l6,{ariaLabel:(0,i.t)("Choose a delimiter"),options:[{value:",",label:'Comma ","'},{value:";",label:'Semicolon ";"'},{value:"\t",label:'Tab "\\t"'},{value:"|",label:"Pipe"}],onChange:e=>{V(e)},allowNewOptions:!0})})})}),q("sheet_name",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{label:(0,i.t)("Sheet name"),name:"sheet_name",children:(0,A.Y)(h.l6,{ariaLabel:(0,i.t)("Choose sheet name"),options:$.map((e=>({value:e,label:e}))),onChange:e=>{var a;k(null!=(a=R[e])?a:[])},allowNewOptions:!0,placeholder:(0,i.t)("Select a sheet name from the uploaded file")})})})})]},"general"),(0,A.FD)(c.A.Panel,{header:(0,A.FD)("div",{children:[(0,A.Y)("h4",{children:(0,i.t)("File settings")}),(0,A.Y)("p",{className:"helper",children:(0,i.t)("Adjust how spaces, blank lines, null values are handled and other file wide settings.")})]}),children:[(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(E,{label:(0,i.t)("If table already exists"),tip:(0,i.t)("What should happen if the table already exists"),name:"already_exists",children:(0,A.Y)(h.l6,{ariaLabel:(0,i.t)("Choose already exists"),options:[{value:"fail",label:"Fail"},{value:"replace",label:"Replace"},{value:"append",label:"Append"}],onChange:()=>{}})})})}),q("column_dates",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{label:(0,i.t)("Columns to be parsed as dates"),name:"column_dates",children:(0,A.Y)(h.l6,{ariaLabel:(0,i.t)("Choose columns to be parsed as dates"),mode:"multiple",options:ie(),allowClear:!0,allowNewOptions:!0,placeholder:(0,i.t)("Select column names from a dropdown list that should be parsed as dates.")})})})}),q("decimal_character",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(E,{label:(0,i.t)("Decimal character"),tip:(0,i.t)("Character to interpret as decimal point"),name:"decimal_character",children:(0,A.Y)(p.pd,{type:"text"})})})}),q("null_values",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(E,{label:(0,i.t)("Null Values"),tip:(0,i.t)("Choose values that should be treated as null. Warning: Hive database supports only a single value"),name:"null_values",children:(0,A.Y)(h.l6,{mode:"multiple",options:[{value:'""',label:'Empty Strings ""'},{value:"None",label:"None"},{value:"nan",label:"nan"},{value:"null",label:"null"},{value:"N/A",label:"N/A"}],allowClear:!0,allowNewOptions:!0})})})}),q("skip_initial_space",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{name:"skip_initial_space",children:(0,A.Y)(L,{label:(0,i.t)("Skip spaces after delimiter"),dataTest:"skipInitialSpace"})})})}),q("skip_blank_lines",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{name:"skip_blank_lines",children:(0,A.Y)(L,{label:(0,i.t)("Skip blank lines rather than interpreting them as Not A Number values"),dataTest:"skipBlankLines"})})})}),q("day_first",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{name:"day_first",children:(0,A.Y)(L,{label:(0,i.t)("DD/MM format dates, international and European format"),dataTest:"dayFirst"})})})})]},"2"),(0,A.FD)(c.A.Panel,{header:(0,A.FD)("div",{children:[(0,A.Y)("h4",{children:(0,i.t)("Columns")}),(0,A.Y)("p",{className:"helper",children:(0,i.t)("Adjust column settings such as specifying the columns to read, how duplicates are handled, column data types, and more.")})]}),children:[(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{label:(0,i.t)("Columns to read"),name:"columns_read",children:(0,A.Y)(h.l6,{ariaLabel:(0,i.t)("Choose columns to read"),mode:"multiple",options:ie(),allowClear:!0,allowNewOptions:!0,placeholder:(0,i.t)("List of the column names that should be read")})})})}),q("column_data_types",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(E,{label:(0,i.t)("Column data types"),tip:(0,i.t)('A dictionary with column names and their data types if you need to change the defaults. Example: {"user_id":"int"}. Check Python\'s Pandas library for supported data types.'),name:"column_data_types",children:(0,A.Y)(p.pd,{"aria-label":(0,i.t)("Column data types"),type:"text"})})})}),(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{name:"dataframe_index",children:(0,A.Y)(L,{label:(0,i.t)("Create dataframe index"),dataTest:"dataFrameIndex",onChange:J})})})}),Q&&q("index_column",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(E,{label:(0,i.t)("Index column"),tip:(0,i.t)("Column to use as the index of the dataframe. If None is given, Index label is used."),name:"index_column",children:(0,A.Y)(h.l6,{ariaLabel:(0,i.t)("Choose index column"),options:N.map((e=>({value:e,label:e}))),allowClear:!0,allowNewOptions:!0})})})}),Q&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(E,{label:(0,i.t)("Index label"),tip:(0,i.t)("Label for the index column. Don't use an existing column name."),name:"index_label",children:(0,A.Y)(p.pd,{"aria-label":(0,i.t)("Index label"),type:"text"})})})})]},"3"),q("header_row",b)&&q("rows_to_read",b)&&q("skip_rows",b)&&(0,A.Y)(c.A.Panel,{header:(0,A.FD)("div",{children:[(0,A.Y)("h4",{children:(0,i.t)("Rows")}),(0,A.Y)("p",{className:"helper",children:(0,i.t)("Set header rows and the number of rows to read or skip.")})]}),children:(0,A.FD)(h.fI,{children:[(0,A.Y)(h.fv,{span:8,children:(0,A.Y)(E,{label:(0,i.t)("Header row"),tip:(0,i.t)("Row containing the headers to use as column names (0 is first line of data)."),name:"header_row",rules:[{required:!0,message:"Header row is required"}],children:(0,A.Y)(p.YI,{"aria-label":(0,i.t)("Header row"),type:"text",min:0})})}),(0,A.Y)(h.fv,{span:8,children:(0,A.Y)(E,{label:(0,i.t)("Rows to read"),tip:(0,i.t)("Number of rows of file to read. Leave empty (default) to read all rows"),name:"rows_to_read",children:(0,A.Y)(p.YI,{"aria-label":(0,i.t)("Rows to read"),min:1})})}),(0,A.Y)(h.fv,{span:8,children:(0,A.Y)(E,{label:(0,i.t)("Skip rows"),tip:(0,i.t)("Number of rows to skip at start of file."),name:"skip_rows",rules:[{required:!0,message:"Skip rows is required"}],children:(0,A.Y)(p.YI,{"aria-label":(0,i.t)("Skip rows"),min:0})})})]})},"4")]})})})}))},31383:(e,a,t)=>{t.d(a,{A:()=>c});var n=t(78518),l=t(50500),r=t(25946),i=t(17437),o=t(2445);const s=(0,l.xK)(),d=s?s.support:"https://superset.apache.org/docs/databases/installing-database-drivers",c=({errorMessage:e,showDbInstallInstructions:a})=>(0,o.Y)(r.A,{closable:!1,css:e=>(e=>i.AH`
  margin: ${4*e.gridUnit}px 0;

  .antd5-alert-message {
    margin: 0;
  }
`)(e),type:"error",showIcon:!0,message:e,description:a?(0,o.FD)(o.FK,{children:[(0,o.Y)("br",{}),(0,n.t)("Database driver for importing maybe not installed. Visit the Superset documentation page for installation instructions: "),(0,o.Y)("a",{href:d,target:"_blank",rel:"noopener noreferrer",className:"additional-fields-alert-description",children:(0,n.t)("here")}),"."]}):""})},43293:(e,a,t)=>{t.d(a,{hT:()=>Je,Ay:()=>ea});var n=t(44383),l=t.n(n),r=t(62193),i=t.n(r),o=t(72391),s=t(96453),d=t(78518),c=t(17437),h=t(96540),u=t(61574),p=t(62221),m=t(48327),g=t(15595),b=t(25946),v=t(85861),f=t(46920),y=t(19129),_=t(91162),x=t(67073),Y=t(2445);const w=({buttonText:e,icon:a,altText:t,...n})=>(0,Y.Y)(_.A,{hoverable:!0,role:"button",tabIndex:0,"aria-label":e,onKeyDown:e=>{"Enter"!==e.key&&" "!==e.key||(n.onClick&&n.onClick(e)," "===e.key&&e.preventDefault()),null==n.onKeyDown||n.onKeyDown(e)},cover:a?(0,Y.Y)("img",{src:a,alt:t||e,css:c.AH`
          width: 100%;
          height: 120px;
          object-fit: contain;
        `}):(0,Y.Y)("div",{css:c.AH`
          display: flex;
          align-content: center;
          align-items: center;
          height: 120px;
        `,children:(0,Y.Y)(x.F.DatabaseOutlined,{css:c.AH`
            font-size: 48px;
          `,"aria-label":"default-icon"})}),css:e=>({padding:3*e.gridUnit,textAlign:"center",...n.style}),...n,children:(0,Y.Y)(y.m_,{title:e,children:(0,Y.Y)(g.o5.Text,{ellipsis:!0,children:e})})});var C,S,A=t(31641),F=t(5261),D=t(97987),N=t(79427),E=t(31383),k=t(50500),$=t(28292),I=t(17444);!function(e){e.SqlalchemyUri="sqlalchemy_form",e.DynamicForm="dynamic_form"}(C||(C={})),function(e){e.GSheet="gsheets",e.BigQuery="bigquery",e.Snowflake="snowflake"}(S||(S={}));var T=t(46942),U=t.n(T),P=t(27366),q=t(85994),O=t(61693),z=t(24976);const M=c.AH`
  margin-bottom: 0;
`,L=s.I4.header`
  padding: ${({theme:e})=>2*e.gridUnit}px
    ${({theme:e})=>4*e.gridUnit}px;
  line-height: ${({theme:e})=>6*e.gridUnit}px;

  .helper-top {
    padding-bottom: 0;
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    margin: 0;
  }

  .subheader-text {
    line-height: ${({theme:e})=>4.25*e.gridUnit}px;
  }

  .helper-bottom {
    padding-top: 0;
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    margin: 0;
  }

  h4 {
    color: ${({theme:e})=>e.colors.grayscale.dark2};
    font-size: ${({theme:e})=>e.typography.sizes.l}px;
    margin: 0;
    padding: 0;
    line-height: ${({theme:e})=>8*e.gridUnit}px;
  }

  .select-db {
    padding-bottom: ${({theme:e})=>2*e.gridUnit}px;
    .helper {
      margin: 0;
    }

    h4 {
      margin: 0 0 ${({theme:e})=>4*e.gridUnit}px;
    }
  }
`,R=c.AH`
  .ant-tabs-top {
    margin-top: 0;
  }
  .ant-tabs-top > .ant-tabs-nav {
    margin-bottom: 0;
  }
  .ant-tabs-tab {
    margin-right: 0;
  }
`,H=c.AH`
  .antd5-modal-body {
    padding-left: 0;
    padding-right: 0;
    padding-top: 0;
  }
`,j=e=>c.AH`
  margin-bottom: ${5*e.gridUnit}px;
  svg {
    margin-bottom: ${.25*e.gridUnit}px;
  }
  display: flex;
`,V=e=>c.AH`
  padding-left: ${2*e.gridUnit}px;
  padding-right: ${2*e.gridUnit}px;
`,B=e=>c.AH`
  padding: ${4*e.gridUnit}px ${4*e.gridUnit}px 0;
`,K=e=>c.AH`
  .ant-select-dropdown {
    height: ${40*e.gridUnit}px;
  }

  .antd5-modal-header {
    padding: ${4.5*e.gridUnit}px ${4*e.gridUnit}px
      ${4*e.gridUnit}px;
  }

  .antd5-modal-close-x .close {
    opacity: 1;
  }

  .antd5-modal-body {
    height: ${180.5*e.gridUnit}px;
  }

  .antd5-modal-footer {
    height: ${16.25*e.gridUnit}px;
  }
`,W=e=>c.AH`
  margin: ${4*e.gridUnit}px 0;
`,G=s.I4.div`
  ${({theme:e})=>c.AH`
    margin: 0 ${4*e.gridUnit}px ${4*e.gridUnit}px;
  `}
`,Q=e=>c.AH`
  .required {
    margin-left: ${e.gridUnit/2}px;
    color: ${e.colors.error.base};
  }

  .helper {
    display: block;
    padding: ${e.gridUnit}px 0;
    color: ${e.colors.grayscale.light1};
    font-size: ${e.typography.sizes.s}px;
    text-align: left;
  }
`,J=e=>c.AH`
  .form-group {
    margin-bottom: ${4*e.gridUnit}px;
    &-w-50 {
      display: inline-block;
      width: ${`calc(50% - ${4*e.gridUnit}px)`};
      & + .form-group-w-50 {
        margin-left: ${8*e.gridUnit}px;
      }
    }
  }
  .control-label {
    color: ${e.colors.grayscale.dark1};
    font-size: ${e.typography.sizes.s}px;
  }
  .helper {
    color: ${e.colors.grayscale.light1};
    font-size: ${e.typography.sizes.s}px;
    margin-top: ${1.5*e.gridUnit}px;
  }
  .ant-tabs-content-holder {
    overflow: auto;
    max-height: 480px;
  }
`,X=e=>c.AH`
  label {
    color: ${e.colors.grayscale.dark1};
    font-size: ${e.typography.sizes.s}px;
    margin-bottom: 0;
  }
`,Z=s.I4.div`
  ${({theme:e})=>c.AH`
    margin-bottom: ${6*e.gridUnit}px;
    &.mb-0 {
      margin-bottom: 0;
    }
    &.mb-8 {
      margin-bottom: ${2*e.gridUnit}px;
    }

    .control-label {
      color: ${e.colors.grayscale.dark1};
      font-size: ${e.typography.sizes.s}px;
      margin-bottom: ${2*e.gridUnit}px;
    }

    &.extra-container {
      padding-top: ${2*e.gridUnit}px;
    }

    .input-container {
      display: flex;
      align-items: top;

      label {
        display: flex;
        margin-left: ${2*e.gridUnit}px;
        margin-top: ${.75*e.gridUnit}px;
        font-family: ${e.typography.families.sansSerif};
        font-size: ${e.typography.sizes.m}px;
      }

      i {
        margin: 0 ${e.gridUnit}px;
      }
    }

    input,
    textarea {
      flex: 1 1 auto;
    }

    textarea {
      height: 160px;
      resize: none;
    }

    input::placeholder,
    textarea::placeholder {
      color: ${e.colors.grayscale.light1};
    }

    textarea,
    input[type='text'],
    input[type='number'] {
      padding: ${1.5*e.gridUnit}px ${2*e.gridUnit}px;
      border-style: none;
      border: 1px solid ${e.colors.grayscale.light2};
      border-radius: ${e.gridUnit}px;

      &[name='name'] {
        flex: 0 1 auto;
        width: 40%;
      }
    }
    &.expandable {
      height: 0;
      overflow: hidden;
      transition: height 0.25s;
      margin-left: ${8*e.gridUnit}px;
      margin-bottom: 0;
      padding: 0;
      .control-label {
        margin-bottom: 0;
      }
      &.open {
        height: ${108}px;
        padding-right: ${5*e.gridUnit}px;
      }
    }
  `}
`,ee=(0,s.I4)(z.iN)`
  flex: 1 1 auto;
  border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
  border-radius: ${({theme:e})=>e.gridUnit}px;
`,ae=s.I4.div`
  padding-top: ${({theme:e})=>e.gridUnit}px;
  .input-container {
    padding-top: ${({theme:e})=>e.gridUnit}px;
    padding-bottom: ${({theme:e})=>e.gridUnit}px;
  }
  &.expandable {
    height: 0;
    overflow: hidden;
    transition: height 0.25s;
    margin-left: ${({theme:e})=>7*e.gridUnit}px;
    &.open {
      height: ${261}px;
      &.ctas-open {
        height: ${363}px;
      }
    }
  }
`,te=s.I4.div`
  padding: 0 ${({theme:e})=>4*e.gridUnit}px;
  margin-top: ${({theme:e})=>6*e.gridUnit}px;
`,ne=e=>c.AH`
  font-weight: ${e.typography.weights.normal};
  text-transform: initial;
  padding-right: ${2*e.gridUnit}px;
`,le=e=>c.AH`
  font-size: ${3.5*e.gridUnit}px;
  font-weight: ${e.typography.weights.normal};
  text-transform: initial;
  padding-right: ${2*e.gridUnit}px;
`,re=s.I4.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0px;

  .helper {
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    margin: 0px;
  }
`,ie=(s.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  font-weight: ${({theme:e})=>e.typography.weights.bold};
  font-size: ${({theme:e})=>e.typography.sizes.m}px;
`,s.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
`,s.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.light1};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
`),oe=s.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
  font-size: ${({theme:e})=>e.typography.sizes.l}px;
  font-weight: ${({theme:e})=>e.typography.weights.bold};
`,se=s.I4.div`
  .catalog-type-select {
    margin: 0 0 20px;
  }

  .label-select {
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    font-size: 11px;
    margin: 0 5px ${({theme:e})=>2*e.gridUnit}px;
  }

  .label-paste {
    color: ${({theme:e})=>e.colors.grayscale.light1};
    font-size: 11px;
    line-height: 16px;
  }

  .input-container {
    margin: ${({theme:e})=>4*e.gridUnit}px 0;
    display: flex;
    flex-direction: column;
}
  }
  .input-form {
    height: 100px;
    width: 100%;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;
    resize: vertical;
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    &::placeholder {
      color: ${({theme:e})=>e.colors.grayscale.light1};
    }
  }

  .input-container {
    width: 100%;

    button {
      width: fit-content;
    }

    .credentials-uploaded {
      display: flex;
      align-items: center;
      gap: ${({theme:e})=>3*e.gridUnit}px;
      width: fit-content;
    }

    .credentials-uploaded-btn, .credentials-uploaded-remove {
      flex: 0 0 auto;
    }

    /* hide native file upload input element */
    .input-upload {
      display: none !important;
    }
  }`,de=s.I4.div`
  .preferred {
    .superset-button {
      margin-left: 0;
    }
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    margin: ${({theme:e})=>4*e.gridUnit}px;
  }

  .preferred-item {
    width: 32%;
    margin-bottom: ${({theme:e})=>2.5*e.gridUnit}px;
  }

  .available {
    margin: ${({theme:e})=>4*e.gridUnit}px;
    .available-label {
      font-size: ${({theme:e})=>e.typography.sizes.l}px;
      font-weight: ${({theme:e})=>e.typography.weights.bold};
      margin: ${({theme:e})=>6*e.gridUnit}px 0;
    }
    .available-select {
      width: 100%;
    }
  }

  .label-available-select {
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
  }

  .control-label {
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }
`,ce=(0,s.I4)(f.A)`
  width: ${({theme:e})=>40*e.gridUnit}px;
`,he=s.I4.div`
  position: sticky;
  top: 0;
  z-index: ${({theme:e})=>e.zIndex.max};
  background: ${({theme:e})=>e.colors.grayscale.light5};
  height: auto;
`,ue=s.I4.div`
  margin-bottom: 16px;

  .catalog-type-select {
    margin: 0 0 20px;
  }

  .gsheet-title {
    font-size: ${({theme:e})=>e.typography.sizes.l}px;
    font-weight: ${({theme:e})=>e.typography.weights.bold};
    margin: ${({theme:e})=>10*e.gridUnit}px 0 16px;
  }

  .catalog-label {
    margin: 0 0 7px;
  }

  .catalog-name {
    display: flex;
    .catalog-name-input {
      width: 95%;
      margin-bottom: 0px;
    }
  }

  .catalog-name-url {
    margin: 4px 0;
    width: 95%;
  }

  .catalog-add-btn {
    width: 95%;
  }
`,pe=s.I4.div`
  .ant-progress-inner {
    display: none;
  }

  .ant-upload-list-item-card-actions {
    display: none;
  }
`,me=({db:e,onInputChange:a,onTextChange:t,onEditorChange:n,onExtraInputChange:l,onExtraEditorChange:r,extraExtension:i})=>{var o,h,u,p,m;const g=!(null==e||!e.expose_in_sqllab),b=!!(null!=e&&e.allow_ctas||null!=e&&e.allow_cvas),v=null==e||null==(o=e.engine_information)?void 0:o.supports_file_upload,f=null==e||null==(h=e.engine_information)?void 0:h.supports_dynamic_catalog,y=JSON.parse((null==e?void 0:e.extra)||"{}",((e,a)=>"engine_params"===e&&"object"==typeof a?JSON.stringify(a):a)),_=(0,s.DP)(),x=null==i?void 0:i.component,w=null==i?void 0:i.logo,C=null==i?void 0:i.description,S=!!(0,P.G7)(P.TO.ForceSqlLabRunAsync)||!(null==e||!e.allow_run_async),F=(0,P.G7)(P.TO.ForceSqlLabRunAsync);return(0,Y.FD)(O.A,{expandIconPosition:"right",accordion:!0,css:e=>(e=>c.AH`
  .ant-collapse-header {
    padding-top: ${3.5*e.gridUnit}px;
    padding-bottom: ${2.5*e.gridUnit}px;

    .anticon.ant-collapse-arrow {
      top: calc(50% - ${6}px);
    }
    .helper {
      color: ${e.colors.grayscale.base};
    }
  }
  h4 {
    font-size: 16px;
    margin-top: 0;
    margin-bottom: ${e.gridUnit}px;
  }
  p.helper {
    margin-bottom: 0;
    padding: 0;
  }
`)(e),children:[(0,Y.Y)(O.A.Panel,{header:(0,Y.FD)("div",{children:[(0,Y.Y)("h4",{children:(0,d.t)("SQL Lab")}),(0,Y.Y)("p",{className:"helper",children:(0,d.t)("Adjust how this database will interact with SQL Lab.")})]}),children:(0,Y.FD)(Z,{css:M,children:[(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(q.A,{id:"expose_in_sqllab",indeterminate:!1,checked:!(null==e||!e.expose_in_sqllab),onChange:a,labelText:(0,d.t)("Expose database in SQL Lab")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Allow this database to be queried in SQL Lab")})]}),(0,Y.FD)(ae,{className:U()("expandable",{open:g,"ctas-open":b}),children:[(0,Y.Y)(Z,{css:M,children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(q.A,{id:"allow_ctas",indeterminate:!1,checked:!(null==e||!e.allow_ctas),onChange:a,labelText:(0,d.t)("Allow CREATE TABLE AS")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Allow creation of new tables based on queries")})]})}),(0,Y.FD)(Z,{css:M,children:[(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(q.A,{id:"allow_cvas",indeterminate:!1,checked:!(null==e||!e.allow_cvas),onChange:a,labelText:(0,d.t)("Allow CREATE VIEW AS")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Allow creation of new views based on queries")})]}),(0,Y.FD)(Z,{className:U()("expandable",{open:b}),children:[(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("CTAS & CVAS SCHEMA")}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)("input",{type:"text",name:"force_ctas_schema",placeholder:(0,d.t)("Create or select schema..."),onChange:a,value:(null==e?void 0:e.force_ctas_schema)||""})}),(0,Y.Y)("div",{className:"helper",children:(0,d.t)("Force all tables and views to be created in this schema when clicking CTAS or CVAS in SQL Lab.")})]})]}),(0,Y.Y)(Z,{css:M,children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(q.A,{id:"allow_dml",indeterminate:!1,checked:!(null==e||!e.allow_dml),onChange:a,labelText:(0,d.t)("Allow DDL and DML")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Allow the execution of DDL (Data Definition Language: CREATE, DROP, TRUNCATE, etc.) and DML (Data Modification Language: INSERT, UPDATE, DELETE, etc)")})]})}),(0,Y.Y)(Z,{css:M,children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(q.A,{id:"cost_estimate_enabled",indeterminate:!1,checked:!(null==y||!y.cost_estimate_enabled),onChange:l,labelText:(0,d.t)("Enable query cost estimation")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("For Bigquery, Presto and Postgres, shows a button to compute cost before running a query.")})]})}),(0,Y.Y)(Z,{css:M,children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(q.A,{id:"allows_virtual_table_explore",indeterminate:!1,checked:!1!==(null==y?void 0:y.allows_virtual_table_explore),onChange:l,labelText:(0,d.t)("Allow this database to be explored")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("When enabled, users are able to visualize SQL Lab results in Explore.")})]})}),(0,Y.Y)(Z,{css:M,children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(q.A,{id:"disable_data_preview",indeterminate:!1,checked:!(null==y||!y.disable_data_preview),onChange:l,labelText:(0,d.t)("Disable SQL Lab data preview queries")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Disable data preview when fetching table metadata in SQL Lab.  Useful to avoid browser performance issues when using  databases with very wide tables.")})]})}),(0,Y.Y)(Z,{children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(q.A,{id:"expand_rows",indeterminate:!1,checked:!(null==y||null==(u=y.schema_options)||!u.expand_rows),onChange:l,labelText:(0,d.t)("Enable row expansion in schemas")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("For Trino, describe full schemas of nested ROW types, expanding them with dotted paths")})]})})]})]})},"1"),(0,Y.FD)(O.A.Panel,{header:(0,Y.FD)("div",{children:[(0,Y.Y)("h4",{children:(0,d.t)("Performance")}),(0,Y.Y)("p",{className:"helper",children:(0,d.t)("Adjust performance settings of this database.")})]}),children:[(0,Y.FD)(Z,{className:"mb-8",children:[(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("Chart cache timeout")}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)("input",{type:"number",name:"cache_timeout",value:(null==e?void 0:e.cache_timeout)||"",placeholder:(0,d.t)("Enter duration in seconds"),onChange:a})}),(0,Y.Y)("div",{className:"helper",children:(0,d.t)("Duration (in seconds) of the caching timeout for charts of this database. A timeout of 0 indicates that the cache never expires, and -1 bypasses the cache. Note this defaults to the global timeout if undefined.")})]}),(0,Y.FD)(Z,{children:[(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("Schema cache timeout")}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)("input",{type:"number",name:"schema_cache_timeout",value:(null==y||null==(p=y.metadata_cache_timeout)?void 0:p.schema_cache_timeout)||"",placeholder:(0,d.t)("Enter duration in seconds"),onChange:l})}),(0,Y.Y)("div",{className:"helper",children:(0,d.t)("Duration (in seconds) of the metadata caching timeout for schemas of this database. If left unset, the cache never expires.")})]}),(0,Y.FD)(Z,{children:[(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("Table cache timeout")}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)("input",{type:"number",name:"table_cache_timeout",value:(null==y||null==(m=y.metadata_cache_timeout)?void 0:m.table_cache_timeout)||"",placeholder:(0,d.t)("Enter duration in seconds"),onChange:l})}),(0,Y.Y)("div",{className:"helper",children:(0,d.t)("Duration (in seconds) of the metadata caching timeout for tables of this database. If left unset, the cache never expires. ")})]}),(0,Y.Y)(Z,{css:(0,c.AH)({no_margin_bottom:M},"",""),children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(q.A,{id:"allow_run_async",indeterminate:!1,checked:S,onChange:a,labelText:(0,d.t)("Asynchronous query execution")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Operate the database in asynchronous mode, meaning that the queries are executed on remote workers as opposed to on the web server itself. This assumes that you have a Celery worker setup as well as a results backend. Refer to the installation docs for more information.")}),F&&(0,Y.Y)(A.A,{iconStyle:{color:_.colors.error.base},tooltip:(0,d.t)("This option has been disabled by the administrator.")})]})}),(0,Y.Y)(Z,{css:(0,c.AH)({no_margin_bottom:M},"",""),children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(q.A,{id:"cancel_query_on_windows_unload",indeterminate:!1,checked:!(null==y||!y.cancel_query_on_windows_unload),onChange:l,labelText:(0,d.t)("Cancel query on window unload event")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Terminate running queries when browser window closed or navigated to another page. Available for Presto, Hive, MySQL, Postgres and Snowflake databases.")})]})})]},"2"),(0,Y.FD)(O.A.Panel,{header:(0,Y.FD)("div",{children:[(0,Y.Y)("h4",{children:(0,d.t)("Security")}),(0,Y.Y)("p",{className:"helper",children:(0,d.t)("Add extra connection information.")})]}),children:[(0,Y.FD)(Z,{children:[(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("Secure extra")}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)(ee,{name:"masked_encrypted_extra",value:(null==e?void 0:e.masked_encrypted_extra)||"",placeholder:(0,d.t)("Secure extra"),onChange:e=>n({json:e,name:"masked_encrypted_extra"}),width:"100%",height:"160px"})}),(0,Y.Y)("div",{className:"helper",children:(0,Y.Y)("div",{children:(0,d.t)("JSON string containing additional connection configuration. This is used to provide connection information for systems like Hive, Presto and BigQuery which do not conform to the username:password syntax normally used by SQLAlchemy.")})})]}),(0,Y.FD)(Z,{children:[(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("Root certificate")}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)("textarea",{name:"server_cert",value:(null==e?void 0:e.server_cert)||"",placeholder:(0,d.t)("Enter CA_BUNDLE"),onChange:t})}),(0,Y.Y)("div",{className:"helper",children:(0,d.t)("Optional CA_BUNDLE contents to validate HTTPS requests. Only available on certain database engines.")})]}),(0,Y.Y)(Z,{css:v?{}:M,children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(q.A,{id:"impersonate_user",indeterminate:!1,checked:!(null==e||!e.impersonate_user),onChange:a,labelText:(0,d.t)("Impersonate logged in user (Presto, Trino, Drill, Hive, and GSheets)")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("If Presto or Trino, all the queries in SQL Lab are going to be executed as the currently logged on user who must have permission to run them. If Hive and hive.server2.enable.doAs is enabled, will run the queries as service account, but impersonate the currently logged on user via hive.server2.proxy.user property.")})]})}),v&&(0,Y.Y)(Z,{css:null!=e&&e.allow_file_upload?{}:M,children:(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)(q.A,{id:"allow_file_upload",indeterminate:!1,checked:!(null==e||!e.allow_file_upload),onChange:a,labelText:(0,d.t)("Allow file uploads to database")})})}),v&&!(null==e||!e.allow_file_upload)&&(0,Y.FD)(Z,{css:M,children:[(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("Schemas allowed for File upload")}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)("input",{type:"text",name:"schemas_allowed_for_file_upload",value:((null==y?void 0:y.schemas_allowed_for_file_upload)||[]).join(","),placeholder:"schema1,schema2",onChange:l})}),(0,Y.Y)("div",{className:"helper",children:(0,d.t)("A comma-separated list of schemas that files are allowed to upload to.")})]})]},"3"),i&&x&&C&&(0,Y.Y)(O.A.Panel,{header:(0,Y.FD)("div",{children:[w&&(0,Y.Y)(w,{}),(0,Y.Y)("span",{css:e=>({fontSize:e.typography.sizes.l,fontWeight:e.typography.weights.bold}),children:null==i?void 0:i.title}),(0,Y.Y)("p",{className:"helper",children:(0,Y.Y)(C,{})})]}),collapsible:null!=i.enabled&&i.enabled()?"icon":"disabled",children:(0,Y.Y)(Z,{css:M,children:(0,Y.Y)(x,{db:e,onEdit:i.onEdit})})},null==i?void 0:i.title),(0,Y.FD)(O.A.Panel,{header:(0,Y.FD)("div",{children:[(0,Y.Y)("h4",{children:(0,d.t)("Other")}),(0,Y.Y)("p",{className:"helper",children:(0,d.t)("Additional settings.")})]}),children:[(0,Y.FD)(Z,{children:[(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("Metadata Parameters")}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)(ee,{name:"metadata_params",placeholder:(0,d.t)("Metadata Parameters"),onChange:e=>r({json:e,name:"metadata_params"}),width:"100%",height:"160px",value:Object.keys((null==y?void 0:y.metadata_params)||{}).length?null==y?void 0:y.metadata_params:""})}),(0,Y.Y)("div",{className:"helper",children:(0,Y.Y)("div",{children:(0,d.t)("The metadata_params object gets unpacked into the sqlalchemy.MetaData call.")})})]}),(0,Y.FD)(Z,{children:[(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("Engine Parameters")}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)(ee,{name:"engine_params",placeholder:(0,d.t)("Engine Parameters"),onChange:e=>r({json:e,name:"engine_params"}),width:"100%",height:"160px",value:Object.keys((null==y?void 0:y.engine_params)||{}).length?null==y?void 0:y.engine_params:""})}),(0,Y.Y)("div",{className:"helper",children:(0,Y.Y)("div",{children:(0,d.t)("The engine_params object gets unpacked into the sqlalchemy.create_engine call.")})})]}),(0,Y.FD)(Z,{children:[(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("Version")}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)("input",{type:"text",name:"version",placeholder:(0,d.t)("Version number"),onChange:l,value:(null==y?void 0:y.version)||""})}),(0,Y.Y)("div",{className:"helper",children:(0,d.t)("Specify the database version. This is used with Presto for query cost estimation, and Dremio for syntax changes, among others.")})]}),(0,Y.Y)(Z,{css:M,children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(q.A,{id:"disable_drill_to_detail",indeterminate:!1,checked:!(null==y||!y.disable_drill_to_detail),onChange:l,labelText:(0,d.t)("Disable drill to detail")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Disables the drill to detail feature for this database.")})]})}),f&&(0,Y.Y)(Z,{css:M,children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(q.A,{id:"allow_multi_catalog",indeterminate:!1,checked:!(null==y||!y.allow_multi_catalog),onChange:l,labelText:(0,d.t)("Allow changing catalogs")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Give access to multiple catalogs in a single database connection.")})]})})]},"4")]})};var ge=t(27588);const be=({db:e,onInputChange:a,testConnection:t,conf:n,testInProgress:l=!1,children:r})=>{var i,o;const s=(null==ge.A||null==(i=ge.A.DB_MODAL_SQLALCHEMY_FORM)?void 0:i.SQLALCHEMY_DOCS_URL)||"https://docs.sqlalchemy.org/en/13/core/engines.html",h=(null==ge.A||null==(o=ge.A.DB_MODAL_SQLALCHEMY_FORM)?void 0:o.SQLALCHEMY_DISPLAY_TEXT)||"SQLAlchemy docs";return(0,Y.FD)(Y.FK,{children:[(0,Y.FD)(Z,{children:[(0,Y.FD)("div",{className:"control-label",children:[(0,d.t)("Display Name"),(0,Y.Y)("span",{className:"required",children:"*"})]}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)("input",{type:"text",name:"database_name",value:(null==e?void 0:e.database_name)||"",placeholder:(0,d.t)("Name your database"),onChange:a})}),(0,Y.Y)("div",{className:"helper",children:(0,d.t)("Pick a name to help you identify this database.")})]}),(0,Y.FD)(Z,{children:[(0,Y.FD)("div",{className:"control-label",children:[(0,d.t)("SQLAlchemy URI"),(0,Y.Y)("span",{className:"required",children:"*"})]}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)("input",{type:"text",name:"sqlalchemy_uri",value:(null==e?void 0:e.sqlalchemy_uri)||"",autoComplete:"off",placeholder:(null==e?void 0:e.sqlalchemy_uri_placeholder)||(0,d.t)("dialect+driver://username:password@host:port/database"),onChange:a})}),(0,Y.FD)("div",{className:"helper",children:[(0,d.t)("Refer to the")," ",(0,Y.Y)("a",{href:s||(null==n?void 0:n.SQLALCHEMY_DOCS_URL)||"",target:"_blank",rel:"noopener noreferrer",children:h||(null==n?void 0:n.SQLALCHEMY_DISPLAY_TEXT)||""})," ",(0,d.t)("for more information on how to structure your URI.")]})]}),r,(0,Y.Y)(f.A,{onClick:t,loading:l,cta:!0,buttonStyle:"link",css:e=>(e=>c.AH`
  width: 100%;
  border: 1px solid ${e.colors.primary.dark2};
  color: ${e.colors.primary.dark2};
  &:hover,
  &:focus {
    border: 1px solid ${e.colors.primary.dark1};
    color: ${e.colors.primary.dark1};
  }
`)(e),children:(0,d.t)("Test connection")})]})};var ve=t(40563),fe=t(75488),ye=t(90868);const _e=e=>c.AH`
  .ant-collapse-header {
    padding-bottom: ${1.5*e.gridUnit}px !important;
    padding-top: ${1.5*e.gridUnit}px !important;
  }
  .anticon.ant-collapse-arrow {
    top: 0 !important;
  }
`,xe={account:{label:"Account",helpText:(0,d.t)("Copy the identifier of the account you are trying to connect to."),placeholder:(0,d.t)("e.g. xy12345.us-east-2.aws")},warehouse:{label:"Warehouse",placeholder:(0,d.t)("e.g. compute_wh"),className:"form-group-w-50"},role:{label:"Role",placeholder:(0,d.t)("e.g. AccountAdmin"),className:"form-group-w-50"}},Ye=({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l,field:r})=>{var i,o;return(0,Y.Y)(D.A,{id:r,name:r,required:e,value:null==l||null==(i=l.parameters)?void 0:i[r],validationMethods:{onBlur:t},errorMessage:null==n?void 0:n[r],placeholder:xe[r].placeholder,helpText:null==(o=xe[r])?void 0:o.helpText,label:xe[r].label||r,onChange:a.onParametersChange,className:xe[r].className||r})};var we,Ce=t(40458);!function(e){e[e.JsonUpload=0]="JsonUpload",e[e.CopyPaste=1]="CopyPaste"}(we||(we={}));const Se={gsheets:"service_account_info",bigquery:"credentials_info"},Ae=({changeMethods:e,isEditMode:a,db:t,editNewDb:n})=>{var l;const r=(0,h.useRef)(null),[i,o]=(0,h.useState)(we.JsonUpload.valueOf()),[s,c]=(0,h.useState)(null),u=!a,p=(null==t?void 0:t.engine)&&Se[t.engine],m=null==t||null==(l=t.parameters)?void 0:l[p],b=m&&"object"==typeof m?JSON.stringify(m):m;return(0,Y.FD)(se,{children:[u&&(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(Ce.A,{children:(0,d.t)("How do you want to enter service account credentials?")}),(0,Y.FD)(g._P,{defaultValue:i,style:{width:"100%"},onChange:e=>o(e),children:[(0,Y.Y)(g._P.Option,{value:we.JsonUpload,children:(0,d.t)("Upload JSON file")}),(0,Y.Y)(g._P.Option,{value:we.CopyPaste,children:(0,d.t)("Copy and Paste JSON credentials")})]})]}),i===we.CopyPaste||a||n?(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(Ce.A,{children:(0,d.t)("Service Account")}),(0,Y.Y)("textarea",{className:"input-form",name:p,value:"boolean"==typeof b?String(b):b,onChange:e.onParametersChange,placeholder:(0,d.t)("Paste content of service credentials JSON file here")})]}):u&&(0,Y.FD)("div",{className:"input-container",css:e=>j(e),children:[!s&&(0,Y.FD)(g.$n,{onClick:()=>{var e;return null==(e=r.current)?void 0:e.click()},children:[(0,Y.Y)(x.F.LinkOutlined,{iconSize:"m"}),(0,d.t)("Upload credentials")]}),s&&(0,Y.FD)("div",{className:"credentials-uploaded",children:[(0,Y.FD)(g.$n,{block:!0,disabled:!0,children:[(0,Y.Y)(x.F.LinkOutlined,{iconSize:"m"}),(0,d.t)("Credentials uploaded")]}),(0,Y.Y)(x.F.DeleteFilled,{iconSize:"m",onClick:()=>{c(null),e.onParametersChange({target:{name:p,value:""}})}})]}),(0,Y.Y)("input",{ref:r,id:"selectedFile",accept:".json",className:"input-upload",type:"file",onChange:async a=>{var t,n;let l;a.target.files&&(l=a.target.files[0]),c(null==(t=l)?void 0:t.name),e.onParametersChange({target:{type:null,name:p,value:await(null==(n=l)?void 0:n.text()),checked:!1}}),r.current&&(r.current.value=null)}})]})]})},Fe=({clearValidationErrors:e,changeMethods:a,db:t,dbModel:n})=>{var l,r,o;const[s,c]=(0,h.useState)(!1),u=(0,P.G7)(P.TO.SshTunneling),p=(null==n||null==(l=n.engine_information)?void 0:l.disable_ssh_tunneling)||!1,m=u&&!p;return(0,h.useEffect)((()=>{var e;m&&void 0!==(null==t||null==(e=t.parameters)?void 0:e.ssh)&&c(t.parameters.ssh)}),[null==t||null==(r=t.parameters)?void 0:r.ssh,m]),(0,h.useEffect)((()=>{var e;m&&void 0===(null==t||null==(e=t.parameters)?void 0:e.ssh)&&!i()(null==t?void 0:t.ssh_tunnel)&&a.onParametersChange({target:{type:"toggle",name:"ssh",checked:!0,value:!0}})}),[a,null==t||null==(o=t.parameters)?void 0:o.ssh,null==t?void 0:t.ssh_tunnel,m]),m?(0,Y.FD)("div",{css:e=>j(e),children:[(0,Y.Y)(fe.d,{checked:s,onChange:t=>{c(t),a.onParametersChange({target:{type:"toggle",name:"ssh",checked:!0,value:t}}),e()}}),(0,Y.Y)("span",{css:V,children:(0,d.t)("SSH Tunnel")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("SSH Tunnel configuration parameters"),placement:"right",viewBox:"0 -5 24 24"})]}):null};var De;const Ne=["host","port","database","default_catalog","default_schema","username","password","access_token","http_path","http_path_field","database_name","project_id","catalog","credentials_info","service_account_info","query","encryption","account","warehouse","role","ssh","oauth2_client_info"],Ee={host:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r;return(0,Y.Y)(D.A,{id:"host",name:"host",value:null==l||null==(r=l.parameters)?void 0:r.host,required:e,hasTooltip:!0,tooltipText:(0,d.t)("This can be either an IP address (e.g. 127.0.0.1) or a domain name (e.g. mydatabase.com)."),validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.host,placeholder:(0,d.t)("e.g. 127.0.0.1"),className:"form-group-w-50",label:(0,d.t)("Host"),onChange:a.onParametersChange})},http_path:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r,i;const o=JSON.parse((null==l?void 0:l.extra)||"{}");return(0,Y.Y)(D.A,{id:"http_path",name:"http_path",required:e,value:null==(r=o.engine_params)||null==(i=r.connect_args)?void 0:i.http_path,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.http_path,placeholder:(0,d.t)("e.g. sql/protocolv1/o/12345"),label:"HTTP Path",onChange:a.onExtraInputChange,helpText:(0,d.t)("Copy the name of the HTTP Path of your cluster.")})},http_path_field:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r;return(0,Y.Y)(D.A,{id:"http_path_field",name:"http_path_field",required:e,value:null==l||null==(r=l.parameters)?void 0:r.http_path_field,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.http_path,placeholder:(0,d.t)("e.g. sql/protocolv1/o/12345"),label:"HTTP Path",onChange:a.onParametersChange,helpText:(0,d.t)("Copy the name of the HTTP Path of your cluster.")})},port:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r;return(0,Y.Y)(Y.FK,{children:(0,Y.Y)(D.A,{id:"port",name:"port",type:"number",required:e,value:null==l||null==(r=l.parameters)?void 0:r.port,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.port,placeholder:(0,d.t)("e.g. 5432"),className:"form-group-w-50",label:(0,d.t)("Port"),onChange:a.onParametersChange})})},database:({required:e,changeMethods:a,getValidation:t,validationErrors:n,placeholder:l,db:r})=>{var i;return(0,Y.Y)(D.A,{id:"database",name:"database",required:e,value:null==r||null==(i=r.parameters)?void 0:i.database,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.database,placeholder:null!=l?l:(0,d.t)("e.g. world_population"),label:(0,d.t)("Database name"),onChange:a.onParametersChange,helpText:(0,d.t)("Copy the name of the database you are trying to connect to.")})},default_catalog:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r;return(0,Y.Y)(D.A,{id:"default_catalog",name:"default_catalog",required:e,value:null==l||null==(r=l.parameters)?void 0:r.default_catalog,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.default_catalog,placeholder:(0,d.t)("e.g. hive_metastore"),label:(0,d.t)("Default Catalog"),onChange:a.onParametersChange,helpText:(0,d.t)("The default catalog that should be used for the connection.")})},default_schema:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r;return(0,Y.Y)(D.A,{id:"default_schema",name:"default_schema",required:e,value:null==l||null==(r=l.parameters)?void 0:r.default_schema,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.default_schema,placeholder:(0,d.t)("e.g. default"),label:(0,d.t)("Default Schema"),onChange:a.onParametersChange,helpText:(0,d.t)("The default schema that should be used for the connection.")})},username:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r;return(0,Y.Y)(D.A,{id:"username",name:"username",required:e,value:null==l||null==(r=l.parameters)?void 0:r.username,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.username,placeholder:(0,d.t)("e.g. Analytics"),label:(0,d.t)("Username"),onChange:a.onParametersChange})},password:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l,isEditMode:r})=>{var i;return(0,Y.Y)(D.A,{id:"password",name:"password",required:e,visibilityToggle:!r,value:null==l||null==(i=l.parameters)?void 0:i.password,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.password,placeholder:(0,d.t)("e.g. ********"),label:(0,d.t)("Password"),onChange:a.onParametersChange})},oauth2_client_info:({changeMethods:e,db:a,default_value:t})=>{var n,l,r,i,o;const s=JSON.parse((null==a?void 0:a.masked_encrypted_extra)||"{}"),[d,c]=(0,h.useState)({id:(null==(n=s.oauth2_client_info)?void 0:n.id)||"",secret:(null==(l=s.oauth2_client_info)?void 0:l.secret)||"",authorization_request_uri:(null==(r=s.oauth2_client_info)?void 0:r.authorization_request_uri)||(null==t?void 0:t.authorization_request_uri)||"",token_request_uri:(null==(i=s.oauth2_client_info)?void 0:i.token_request_uri)||(null==t?void 0:t.token_request_uri)||"",scope:(null==(o=s.oauth2_client_info)?void 0:o.scope)||(null==t?void 0:t.scope)||""}),u=a=>t=>{const n={...d,[a]:t.target.value};c(n);const l={target:{type:"object",name:"oauth2_client_info",value:n}};e.onParametersChange(l)};return(0,Y.Y)(O.A,{children:(0,Y.FD)(O.A.Panel,{header:"OAuth2 client information",css:_e,children:[(0,Y.Y)(ve.eI,{label:"Client ID",children:(0,Y.Y)(ye.pd,{value:d.id,onChange:u("id")})}),(0,Y.Y)(ve.eI,{label:"Client Secret",children:(0,Y.Y)(ye.pd,{type:"password",value:d.secret,onChange:u("secret")})}),(0,Y.Y)(ve.eI,{label:"Authorization Request URI",children:(0,Y.Y)(ye.pd,{placeholder:"https://",value:d.authorization_request_uri,onChange:u("authorization_request_uri")})}),(0,Y.Y)(ve.eI,{label:"Token Request URI",children:(0,Y.Y)(ye.pd,{placeholder:"https://",value:d.token_request_uri,onChange:u("token_request_uri")})}),(0,Y.Y)(ve.eI,{label:"Scope",children:(0,Y.Y)(ye.pd,{value:d.scope,onChange:u("scope")})})]},"1")})},access_token:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l,isEditMode:r,default_value:i,description:o})=>{var s;return(0,Y.Y)(D.A,{id:"access_token",name:"access_token",required:e,visibilityToggle:!r,value:null==l||null==(s=l.parameters)?void 0:s.access_token,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.access_token,placeholder:(0,d.t)("Paste your access token here"),get_url:"string"==typeof i&&i.includes("https://")?i:null,description:o,label:(0,d.t)("Access token"),onChange:a.onParametersChange})},database_name:({changeMethods:e,getValidation:a,validationErrors:t,db:n})=>(0,Y.Y)(Y.FK,{children:(0,Y.Y)(D.A,{id:"database_name",name:"database_name",required:!0,value:null==n?void 0:n.database_name,validationMethods:{onBlur:a},errorMessage:null==t?void 0:t.database_name,placeholder:"",label:(0,d.t)("Display Name"),onChange:e.onChange,helpText:(0,d.t)("Pick a nickname for how the database will display in Superset.")})}),query:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>(0,Y.Y)(D.A,{id:"query_input",name:"query_input",required:e,value:(null==l?void 0:l.query_input)||"",validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.query,placeholder:(0,d.t)("e.g. param1=value1&param2=value2"),label:(0,d.t)("Additional Parameters"),onChange:a.onQueryChange,helpText:(0,d.t)("Add additional custom parameters")}),encryption:({isEditMode:e,changeMethods:a,db:t,sslForced:n})=>{var l;return(0,Y.FD)("div",{css:e=>j(e),children:[(0,Y.Y)(fe.d,{disabled:n&&!e,checked:(null==t||null==(l=t.parameters)?void 0:l.encryption)||n,onChange:e=>{a.onParametersChange({target:{type:"toggle",name:"encryption",checked:!0,value:e}})}}),(0,Y.Y)("span",{css:V,children:"SSL"}),(0,Y.Y)(A.A,{tooltip:(0,d.t)('SSL Mode "require" will be used.'),placement:"right",viewBox:"0 -5 24 24"})]})},credentials_info:Ae,service_account_info:Ae,catalog:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{const r=(null==l?void 0:l.catalog)||[],i=n||{};return(0,Y.FD)(ue,{children:[(0,Y.Y)("h4",{className:"gsheet-title",children:(0,d.t)("Connect Google Sheets as tables to this database")}),(0,Y.FD)("div",{children:[null==r?void 0:r.map(((n,l)=>{var o,s;return(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(Ce.A,{className:"catalog-label",children:(0,d.t)("Google Sheet Name and URL")}),(0,Y.FD)("div",{className:"catalog-name",children:[(0,Y.Y)(D.A,{className:"catalog-name-input",required:e,validationMethods:{onBlur:t},errorMessage:null==(o=i[l])?void 0:o.name,placeholder:(0,d.t)("Enter a name for this sheet"),onChange:e=>{a.onParametersChange({target:{type:`catalog-${l}`,name:"name",value:e.target.value}})},value:n.name}),(null==r?void 0:r.length)>1&&(0,Y.Y)(x.F.CloseOutlined,{css:e=>c.AH`
                    align-self: center;
                    background: ${e.colors.grayscale.light4};
                    margin: 5px 5px 8px 5px;

                    &.anticon > * {
                      line-height: 0;
                    }
                  `,iconSize:"m",onClick:()=>a.onRemoveTableCatalog(l)})]}),(0,Y.Y)(D.A,{className:"catalog-name-url",required:e,validationMethods:{onBlur:t},errorMessage:null==(s=i[l])?void 0:s.url,placeholder:(0,d.t)("Paste the shareable Google Sheet URL here"),onChange:e=>a.onParametersChange({target:{type:`catalog-${l}`,name:"value",value:e.target.value}}),value:n.value})]})})),(0,Y.FD)(ce,{className:"catalog-add-btn",onClick:()=>{a.onAddTableCatalog()},children:["+ ",(0,d.t)("Add sheet")]})]}),(0,Y.Y)("div",{className:"helper",children:(0,Y.Y)("div",{children:(0,d.t)("In order to connect to non-public sheets you need to either provide a service account or configure an OAuth2 client.")})})]})},warehouse:Ye,role:Ye,account:Ye,ssh:null!=(De=(0,o.a)().get("ssh_tunnel.form.switch"))?De:Fe,project_id:({changeMethods:e,getValidation:a,validationErrors:t,db:n})=>{var l;return(0,Y.Y)(Y.FK,{children:(0,Y.Y)(D.A,{id:"project_id",name:"project_id",required:!0,value:null==n||null==(l=n.parameters)?void 0:l.project_id,validationMethods:{onBlur:a},errorMessage:null==t?void 0:t.project_id,placeholder:"your-project-1234-a1",label:(0,d.t)("Project Id"),onChange:e.onParametersChange,helpText:(0,d.t)("Enter the unique project id for your database.")})})}},ke=({dbModel:e,db:a,editNewDb:t,getPlaceholder:n,getValidation:l,isEditMode:r=!1,onAddTableCatalog:i,onChange:o,onExtraInputChange:s,onEncryptedExtraInputChange:d,onParametersChange:c,onParametersUploadFileChange:h,onQueryChange:u,onRemoveTableCatalog:p,sslForced:m,validationErrors:g,clearValidationErrors:b})=>{const v=null==e?void 0:e.parameters;return(0,Y.Y)(ve.lV,{children:(0,Y.Y)("div",{css:e=>[B,X(e)],children:v&&Ne.filter((e=>Object.keys(v.properties).includes(e)||"database_name"===e)).map((e=>{var f,y,_;return Ee[e]({required:null==(f=v.required)?void 0:f.includes(e),changeMethods:{onParametersChange:c,onChange:o,onQueryChange:u,onParametersUploadFileChange:h,onAddTableCatalog:i,onRemoveTableCatalog:p,onExtraInputChange:s,onEncryptedExtraInputChange:d},validationErrors:g,getValidation:l,clearValidationErrors:b,db:a,key:e,field:e,default_value:null==(y=v.properties[e])?void 0:y.default,description:null==(_=v.properties[e])?void 0:_.description,isEditMode:r,sslForced:m,editNewDb:t,placeholder:n?n(e):void 0})}))})})},$e=(0,k.xK)(),Ie=$e?$e.support:"https://superset.apache.org/docs/configuration/databases#installing-database-drivers",Te={postgresql:"https://superset.apache.org",mssql:"https://superset.apache.org/docs/databases/sql-server",gsheets:"https://superset.apache.org/docs/databases/google-sheets"},Ue=({isLoading:e,isEditMode:a,useSqlAlchemyForm:t,hasConnectedDb:n,db:l,dbName:r,dbModel:i,editNewDb:o,fileList:s})=>{const c=s&&(null==s?void 0:s.length)>0,h=(0,Y.FD)(L,{children:[(0,Y.Y)(ie,{children:null==l?void 0:l.backend}),(0,Y.Y)(oe,{children:r})]}),u=(0,Y.FD)(L,{children:[(0,Y.Y)("p",{className:"helper-top",children:(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:2,stepLast:2})}),(0,Y.Y)("h4",{children:(0,d.t)("Enter Primary Credentials")}),(0,Y.FD)("p",{className:"helper-bottom",children:[(0,d.t)("Need help? Learn how to connect your database")," ",(0,Y.Y)("a",{href:(null==$e?void 0:$e.default)||Ie,target:"_blank",rel:"noopener noreferrer",children:(0,d.t)("here")}),"."]})]}),p=(0,Y.Y)(he,{children:(0,Y.FD)(L,{children:[(0,Y.Y)("p",{className:"helper-top",children:(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:3,stepLast:3})}),(0,Y.Y)("h4",{className:"step-3-text",children:(0,d.t)("Database connected")}),(0,Y.Y)("p",{className:"subheader-text",children:(0,d.t)("Create a dataset to begin visualizing your data as a chart or go to\n          SQL Lab to query your data.")})]})}),m=(0,Y.Y)(he,{children:(0,Y.FD)(L,{children:[(0,Y.Y)("p",{className:"helper-top",children:(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:2,stepLast:3})}),(0,Y.Y)("h4",{children:(0,d.t)("Enter the required %(dbModelName)s credentials",{dbModelName:i.name})}),(0,Y.FD)("p",{className:"helper-bottom",children:[(0,d.t)("Need help? Learn more about")," ",(0,Y.FD)("a",{href:(g=null==l?void 0:l.engine,g?$e?$e[g]||$e.default:Te[g]?Te[g]:`https://superset.apache.org/docs/databases/${g}`:null),target:"_blank",rel:"noopener noreferrer",children:[(0,d.t)("connecting to %(dbModelName)s",{dbModelName:i.name}),"."]})]})]})});var g;const b=(0,Y.Y)(L,{children:(0,Y.FD)("div",{className:"select-db",children:[(0,Y.Y)("p",{className:"helper-top",children:(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:1,stepLast:3})}),(0,Y.Y)("h4",{children:(0,d.t)("Select a database to connect")})]})}),v=(0,Y.Y)(he,{children:(0,Y.FD)(L,{children:[(0,Y.Y)("p",{className:"helper-top",children:(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:2,stepLast:2})}),(0,Y.Y)("h4",{children:(0,d.t)("Enter the required %(dbModelName)s credentials",{dbModelName:i.name})}),(0,Y.Y)("p",{className:"helper-bottom",children:c?s[0].name:""})]})});return c?v:e?(0,Y.Y)(Y.FK,{}):a?h:t?u:n&&!o?p:l||o?m:b};var Pe=t(78697),qe=t(36255),Oe=t(27236);const ze=s.I4.div`
  padding-top: ${({theme:e})=>2*e.gridUnit}px;
  label {
    color: ${({theme:e})=>e.colors.grayscale.base};
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }
`,Me=(0,s.I4)(g.fI)`
  padding-bottom: ${({theme:e})=>2*e.gridUnit}px;
`,Le=(0,s.I4)(g.Wq.Item)`
  margin-bottom: 0 !important;
`,Re=(0,s.I4)(qe.A.Password)`
  margin: ${({theme:e})=>`${e.gridUnit}px 0 ${2*e.gridUnit}px`};
`,He=({db:e,onSSHTunnelParametersChange:a,setSSHTunnelLoginMethod:t})=>{var n,l,r,i,o,s;const[c,u]=(0,h.useState)(Je.Password);return(0,Y.FD)(ve.lV,{children:[(0,Y.FD)(Me,{gutter:16,children:[(0,Y.Y)(g.fv,{xs:24,md:12,children:(0,Y.FD)(ze,{children:[(0,Y.Y)(ve.lR,{htmlFor:"server_address",required:!0,children:(0,d.t)("SSH Host")}),(0,Y.Y)(ye.pd,{name:"server_address",type:"text",placeholder:(0,d.t)("e.g. 127.0.0.1"),value:(null==e||null==(n=e.ssh_tunnel)?void 0:n.server_address)||"",onChange:a})]})}),(0,Y.Y)(g.fv,{xs:24,md:12,children:(0,Y.FD)(ze,{children:[(0,Y.Y)(ve.lR,{htmlFor:"server_port",required:!0,children:(0,d.t)("SSH Port")}),(0,Y.Y)(ye.pd,{name:"server_port",placeholder:(0,d.t)("22"),type:"number",value:null==e||null==(l=e.ssh_tunnel)?void 0:l.server_port,onChange:a})]})})]}),(0,Y.Y)(Me,{gutter:16,children:(0,Y.Y)(g.fv,{xs:24,children:(0,Y.FD)(ze,{children:[(0,Y.Y)(ve.lR,{htmlFor:"username",required:!0,children:(0,d.t)("Username")}),(0,Y.Y)(ye.pd,{name:"username",type:"text",placeholder:(0,d.t)("e.g. Analytics"),value:(null==e||null==(r=e.ssh_tunnel)?void 0:r.username)||"",onChange:a})]})})}),(0,Y.Y)(Me,{gutter:16,children:(0,Y.Y)(g.fv,{xs:24,children:(0,Y.FD)(ze,{children:[(0,Y.Y)(ve.lR,{htmlFor:"use_password",required:!0,children:(0,d.t)("Login with")}),(0,Y.Y)(Le,{name:"use_password",initialValue:c,children:(0,Y.FD)(Pe.s.Group,{onChange:({target:{value:e}})=>{u(e),t(e)},children:[(0,Y.Y)(Pe.s,{value:Je.Password,children:(0,d.t)("Password")}),(0,Y.Y)(Pe.s,{value:Je.PrivateKey,children:(0,d.t)("Private Key & Password")})]})})]})})}),c===Je.Password&&(0,Y.Y)(Me,{gutter:16,children:(0,Y.Y)(g.fv,{xs:24,children:(0,Y.FD)(ze,{children:[(0,Y.Y)(ve.lR,{htmlFor:"password",required:!0,children:(0,d.t)("SSH Password")}),(0,Y.Y)(Re,{name:"password",placeholder:(0,d.t)("e.g. ********"),value:(null==e||null==(i=e.ssh_tunnel)?void 0:i.password)||"",onChange:a,iconRender:e=>e?(0,Y.Y)(Oe.A,{title:"Hide password.",children:(0,Y.Y)(x.F.EyeInvisibleOutlined,{})}):(0,Y.Y)(Oe.A,{title:"Show password.",children:(0,Y.Y)(x.F.EyeOutlined,{})}),role:"textbox"})]})})}),c===Je.PrivateKey&&(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(Me,{gutter:16,children:(0,Y.Y)(g.fv,{xs:24,children:(0,Y.FD)(ze,{children:[(0,Y.Y)(ve.lR,{htmlFor:"private_key",required:!0,children:(0,d.t)("Private Key")}),(0,Y.Y)(ye.fs,{name:"private_key",placeholder:(0,d.t)("Paste Private Key here"),value:(null==e||null==(o=e.ssh_tunnel)?void 0:o.private_key)||"",onChange:a,rows:4})]})})}),(0,Y.Y)(Me,{gutter:16,children:(0,Y.Y)(g.fv,{xs:24,children:(0,Y.FD)(ze,{children:[(0,Y.Y)(ve.lR,{htmlFor:"private_key_password",required:!0,children:(0,d.t)("Private Key Password")}),(0,Y.Y)(Re,{name:"private_key_password",placeholder:(0,d.t)("e.g. ********"),value:(null==e||null==(s=e.ssh_tunnel)?void 0:s.private_key_password)||"",onChange:a,iconRender:e=>e?(0,Y.Y)(Oe.A,{title:"Hide password.",children:(0,Y.Y)(x.F.EyeInvisibleOutlined,{})}):(0,Y.Y)(Oe.A,{title:"Show password.",children:(0,Y.Y)(x.F.EyeOutlined,{})}),role:"textbox"})]})})})]})]})},je=(0,o.a)(),Ve=JSON.stringify({allows_virtual_table_explore:!0}),Be={[S.GSheet]:{message:"Why do I need to create a database?",description:"To begin using your Google Sheets, you need to create a database first. Databases are used as a way to identify your data so that it can be queried and visualized. This database will hold all of your individual Google Sheets you choose to connect here."}},Ke=(0,s.I4)(m.Ay)`
  .ant-tabs-content {
    display: flex;
    width: 100%;
    overflow: inherit;

    & > .ant-tabs-tabpane {
      position: relative;
    }
  }
`,We=s.I4.div`
  ${({theme:e})=>`\n    margin: ${8*e.gridUnit}px ${4*e.gridUnit}px;\n  `};
`,Ge=s.I4.div`
  ${({theme:e})=>`\n    padding: 0px ${4*e.gridUnit}px;\n  `};
`;var Qe,Je;!function(e){e[e.AddTableCatalogSheet=0]="AddTableCatalogSheet",e[e.ConfigMethodChange=1]="ConfigMethodChange",e[e.DbSelected=2]="DbSelected",e[e.EditorChange=3]="EditorChange",e[e.ExtraEditorChange=4]="ExtraEditorChange",e[e.ExtraInputChange=5]="ExtraInputChange",e[e.EncryptedExtraInputChange=6]="EncryptedExtraInputChange",e[e.Fetched=7]="Fetched",e[e.InputChange=8]="InputChange",e[e.ParametersChange=9]="ParametersChange",e[e.QueryChange=10]="QueryChange",e[e.RemoveTableCatalogSheet=11]="RemoveTableCatalogSheet",e[e.Reset=12]="Reset",e[e.TextChange=13]="TextChange",e[e.ParametersSSHTunnelChange=14]="ParametersSSHTunnelChange",e[e.SetSSHTunnelLoginMethod=15]="SetSSHTunnelLoginMethod",e[e.RemoveSSHTunnelConfig=16]="RemoveSSHTunnelConfig"}(Qe||(Qe={})),function(e){e[e.Password=0]="Password",e[e.PrivateKey=1]="PrivateKey"}(Je||(Je={}));const Xe=s.I4.div`
  margin-bottom: ${({theme:e})=>3*e.gridUnit}px;
  margin-left: ${({theme:e})=>3*e.gridUnit}px;
`;function Ze(e,a){var t,n,r,i;const o={...e||{}};let s,d,c={},h="";const u=JSON.parse(o.extra||"{}");switch(a.type){case Qe.ExtraEditorChange:try{d=JSON.parse(a.payload.json||"{}")}catch(e){d=a.payload.json}return{...o,extra:JSON.stringify({...u,[a.payload.name]:d})};case Qe.EncryptedExtraInputChange:return{...o,masked_encrypted_extra:JSON.stringify({...JSON.parse(o.masked_encrypted_extra||"{}"),[a.payload.name]:a.payload.value})};case Qe.ExtraInputChange:return"schema_cache_timeout"===a.payload.name||"table_cache_timeout"===a.payload.name?{...o,extra:JSON.stringify({...u,metadata_cache_timeout:{...null==u?void 0:u.metadata_cache_timeout,[a.payload.name]:a.payload.value}})}:"schemas_allowed_for_file_upload"===a.payload.name?{...o,extra:JSON.stringify({...u,schemas_allowed_for_file_upload:(a.payload.value||"").split(",").filter((e=>""!==e))})}:"http_path"===a.payload.name?{...o,extra:JSON.stringify({...u,engine_params:{connect_args:{[a.payload.name]:null==(p=a.payload.value)?void 0:p.trim()}}})}:"expand_rows"===a.payload.name?{...o,extra:JSON.stringify({...u,schema_options:{...null==u?void 0:u.schema_options,[a.payload.name]:!!a.payload.value}})}:{...o,extra:JSON.stringify({...u,[a.payload.name]:"checkbox"===a.payload.type?a.payload.checked:a.payload.value})};var p;case Qe.InputChange:return"checkbox"===a.payload.type?{...o,[a.payload.name]:a.payload.checked}:{...o,[a.payload.name]:a.payload.value};case Qe.ParametersChange:if(null!=(t=a.payload.type)&&t.startsWith("catalog")&&void 0!==o.catalog){var m;const e=[...o.catalog],t=null==(m=a.payload.type)?void 0:m.split("-")[1],n=e[parseInt(t,10)]||{};return void 0!==a.payload.value&&(n[a.payload.name]=a.payload.value),e.splice(parseInt(t,10),1,n),s=e.reduce(((e,a)=>{const t={...e};return t[a.name]=a.value,t}),{}),{...o,catalog:e,parameters:{...o.parameters,catalog:s}}}return{...o,parameters:{...o.parameters,[a.payload.name]:a.payload.value}};case Qe.ParametersSSHTunnelChange:return{...o,ssh_tunnel:{...o.ssh_tunnel,[a.payload.name]:a.payload.value}};case Qe.SetSSHTunnelLoginMethod:{let e={};var g,b,v;return null!=o&&o.ssh_tunnel&&(e=l()(o.ssh_tunnel,["id","server_address","server_port","username"])),a.payload.login_method===Je.PrivateKey?{...o,ssh_tunnel:{private_key:null==o||null==(g=o.ssh_tunnel)?void 0:g.private_key,private_key_password:null==o||null==(b=o.ssh_tunnel)?void 0:b.private_key_password,...e}}:a.payload.login_method===Je.Password?{...o,ssh_tunnel:{password:null==o||null==(v=o.ssh_tunnel)?void 0:v.password,...e}}:{...o}}case Qe.RemoveSSHTunnelConfig:return{...o,ssh_tunnel:void 0};case Qe.AddTableCatalogSheet:return void 0!==o.catalog?{...o,catalog:[...o.catalog,{name:"",value:""}]}:{...o,catalog:[{name:"",value:""}]};case Qe.RemoveTableCatalogSheet:return null==(n=o.catalog)||n.splice(a.payload.indexToDelete,1),{...o};case Qe.EditorChange:return{...o,[a.payload.name]:a.payload.json};case Qe.QueryChange:return{...o,parameters:{...o.parameters,query:Object.fromEntries(new URLSearchParams(a.payload.value))},query_input:a.payload.value};case Qe.TextChange:return{...o,[a.payload.name]:a.payload.value};case Qe.Fetched:if(c=(null==(r=a.payload)||null==(i=r.parameters)?void 0:i.query)||{},h=Object.entries(c).map((([e,a])=>`${e}=${a}`)).join("&"),a.payload.masked_encrypted_extra&&a.payload.configuration_method===C.DynamicForm){var f;const e=null==(f={...JSON.parse(a.payload.extra||"{}")}.engine_params)?void 0:f.catalog,t=Object.entries(e||{}).map((([e,a])=>({name:e,value:a})));return{...a.payload,engine:a.payload.backend||o.engine,configuration_method:a.payload.configuration_method,catalog:t,parameters:{...a.payload.parameters||o.parameters,catalog:e},query_input:h}}return{...a.payload,masked_encrypted_extra:a.payload.masked_encrypted_extra||"",engine:a.payload.backend||o.engine,configuration_method:a.payload.configuration_method,parameters:a.payload.parameters||o.parameters,ssh_tunnel:a.payload.ssh_tunnel||o.ssh_tunnel,query_input:h};case Qe.DbSelected:return{...a.payload,extra:Ve,expose_in_sqllab:!0};case Qe.ConfigMethodChange:return{...a.payload};case Qe.Reset:default:return null}}const ea=(0,F.Ay)((({addDangerToast:e,addSuccessToast:a,onDatabaseAdd:t,onHide:n,show:l,databaseId:r,dbEngine:o})=>{var y,_,F,T;const U=(0,s.DP)(),[P,q]=(0,h.useReducer)(Ze,null),{state:{loading:O,resource:z,error:M},fetchResource:L,createResource:V,updateResource:X,clearError:Z}=(0,k.fn)("database",(0,d.t)("database"),e,"connection"),[ee,ae]=(0,h.useState)("1"),[ie,oe]=(0,k.d5)(),[se,ue,ge]=(0,k.Y8)(),[ve,fe]=(0,h.useState)(!1),[ye,_e]=(0,h.useState)(!1),[xe,Ye]=(0,h.useState)(""),[we,Ce]=(0,h.useState)(!1),[Se,Ae]=(0,h.useState)(!1),[De,Ne]=(0,h.useState)(!1),[Ee,$e]=(0,h.useState)({}),[Te,Pe]=(0,h.useState)({}),[qe,Oe]=(0,h.useState)({}),[ze,Me]=(0,h.useState)({}),[Le,Re]=(0,h.useState)(!1),[Ve,Je]=(0,h.useState)([]),[ea,aa]=(0,h.useState)(!1),[ta,na]=(0,h.useState)(),[la,ra]=(0,h.useState)([]),[ia,oa]=(0,h.useState)([]),[sa,da]=(0,h.useState)([]),[ca,ha]=(0,h.useState)([]),[ua,pa]=(0,h.useState)({}),ma=null!=(y=je.get("ssh_tunnel.form.switch"))?y:Fe,[ga,ba]=(0,h.useState)(void 0);let va=je.get("databaseconnection.extraOption");va&&(va={...va,onEdit:e=>{pa({...ua,...e})}});const fa=(0,$.B)(),ya=(0,k.g9)(),_a=(0,k.Fp)(),xa=!!r,Ya=_a||!(null==P||!P.engine||!Be[P.engine]),wa=(null==P?void 0:P.configuration_method)===C.SqlalchemyUri,Ca=xa||wa,Sa=se||M,Aa=(0,u.W6)(),Fa=(null==ie||null==(_=ie.databases)?void 0:_.find((e=>e.engine===(xa?null==P?void 0:P.backend:null==P?void 0:P.engine)&&e.default_driver===(null==P?void 0:P.driver))))||(null==ie||null==(F=ie.databases)?void 0:F.find((e=>e.engine===(xa?null==P?void 0:P.backend:null==P?void 0:P.engine))))||{},Da=e=>{if("database"===e)return(0,d.t)("e.g. world_population")},Na=(0,h.useCallback)(((e,a)=>{q({type:e,payload:a})}),[]),Ea=(0,h.useCallback)((()=>{ge(null)}),[ge]),ka=(0,h.useCallback)((({target:e})=>{Na(Qe.ParametersChange,{type:e.type,name:e.name,checked:e.checked,value:e.value})}),[Na]),$a=()=>{q({type:Qe.Reset}),fe(!1),Ea(),Z(),Ce(!1),Je([]),aa(!1),na(""),ra([]),oa([]),da([]),ha([]),$e({}),Pe({}),Oe({}),Me({}),Re(!1),ba(void 0),n()},Ia=e=>{Aa.push(e)},{state:{alreadyExists:Ta,passwordsNeeded:Ua,sshPasswordNeeded:Pa,sshPrivateKeyNeeded:qa,sshPrivateKeyPasswordNeeded:Oa,loading:za,failed:Ma},importResource:La}=(0,k.bN)("database",(0,d.t)("database"),(e=>{na(e)})),Ra=async()=>{var n,l;let r;if(Ae(!0),null==(n=va)||n.onSave(ua,P).then((({error:a})=>{a&&(r=a,e(a))})),r)return void Ae(!1);const o={...P||{}};if(o.configuration_method===C.DynamicForm){var s,c;null!=o&&null!=(s=o.parameters)&&s.catalog&&(o.extra=JSON.stringify({...JSON.parse(o.extra||"{}"),engine_params:{catalog:o.parameters.catalog}}));const a=await ue(o,!0);if(!i()(se)||null!=a&&a.length)return e((0,d.t)("Connection failed, please check your connection settings.")),void Ae(!1);const t=xa?null==(c=o.parameters_schema)?void 0:c.properties:null==Fa?void 0:Fa.parameters.properties,n=JSON.parse(o.masked_encrypted_extra||"{}");Object.keys(t||{}).forEach((e=>{var a,l,r,i;t[e]["x-encrypted-extra"]&&null!=(a=o.parameters)&&a[e]&&("object"==typeof(null==(l=o.parameters)?void 0:l[e])?(n[e]=null==(r=o.parameters)?void 0:r[e],o.parameters[e]=JSON.stringify(o.parameters[e])):n[e]=JSON.parse((null==(i=o.parameters)?void 0:i[e])||"{}"))})),o.masked_encrypted_extra=JSON.stringify(n),o.engine===S.GSheet&&(o.impersonate_user=!0)}if(null!=o&&null!=(l=o.parameters)&&l.catalog&&(o.extra=JSON.stringify({...JSON.parse(o.extra||"{}"),engine_params:{catalog:o.parameters.catalog}})),!1===ga&&(o.ssh_tunnel=null),null!=P&&P.id){if(await X(P.id,o,o.configuration_method===C.DynamicForm)){var h;if(t&&t(),null==(h=va)||h.onSave(ua,P).then((({error:a})=>{a&&(r=a,e(a))})),r)return void Ae(!1);we||($a(),a((0,d.t)("Database settings updated")))}}else if(P){if(await V(o,o.configuration_method===C.DynamicForm)){var u;if(fe(!0),t&&t(),null==(u=va)||u.onSave(ua,P).then((({error:a})=>{a&&(r=a,e(a))})),r)return void Ae(!1);Ca&&($a(),a((0,d.t)("Database connected")))}}else{if(aa(!0),!(Ve[0].originFileObj instanceof File))return;await La(Ve[0].originFileObj,Ee,Te,qe,ze,Le)&&(t&&t(),$a(),a((0,d.t)("Database connected")))}_e(!0),Ce(!1),Ae(!1)},Ha=e=>{if("Other"===e)q({type:Qe.DbSelected,payload:{database_name:e,configuration_method:C.SqlalchemyUri,engine:void 0,engine_information:{supports_file_upload:!0}}});else{const a=null==ie?void 0:ie.databases.filter((a=>a.name===e))[0],{engine:t,parameters:n,engine_information:l,default_driver:r,sqlalchemy_uri_placeholder:i}=a,o=void 0!==n;q({type:Qe.DbSelected,payload:{database_name:e,engine:t,configuration_method:o?C.DynamicForm:C.SqlalchemyUri,engine_information:l,driver:r,sqlalchemy_uri_placeholder:i}}),t===S.GSheet&&q({type:Qe.AddTableCatalogSheet})}},ja=()=>{z&&L(z.id),_e(!1),Ce(!0)},Va=()=>{we&&fe(!1),ea&&aa(!1),Ma&&(aa(!1),na(""),ra([]),oa([]),da([]),ha([]),$e({}),Pe({}),Oe({}),Me({})),q({type:Qe.Reset}),Je([])},Ba=()=>P?!ve||we?(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(ce,{onClick:Va,children:(0,d.t)("Back")},"back"),(0,Y.Y)(ce,{buttonStyle:"primary",onClick:Ra,loading:Se,children:(0,d.t)("Connect")},"submit")]}):(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(ce,{onClick:ja,children:(0,d.t)("Back")},"back"),(0,Y.Y)(ce,{buttonStyle:"primary",onClick:Ra,loading:Se,children:(0,d.t)("Finish")},"submit")]}):ea?(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(ce,{onClick:Va,children:(0,d.t)("Back")},"back"),(0,Y.Y)(ce,{buttonStyle:"primary",onClick:Ra,disabled:!!(za||Ta.length&&!Le||Ua.length&&"{}"===JSON.stringify(Ee)||Pa.length&&"{}"===JSON.stringify(Te)||qa.length&&"{}"===JSON.stringify(qe)||Oa.length&&"{}"===JSON.stringify(ze)),loading:Se,children:(0,d.t)("Connect")},"submit")]}):(0,Y.Y)(Y.FK,{}),Ka=(0,h.useRef)(!0);(0,h.useEffect)((()=>{Ka.current?Ka.current=!1:za||Ta.length||Ua.length||Pa.length||qa.length||Oa.length||Se||Ma||($a(),a((0,d.t)("Database connected")))}),[Ta,Ua,za,Ma,Pa,qa,Oa]),(0,h.useEffect)((()=>{l&&(ae("1"),Ae(!0),oe()),r&&l&&xa&&r&&(O||L(r).catch((a=>e((0,d.t)("Sorry there was an error fetching database information: %s",a.message)))))}),[l,r]),(0,h.useEffect)((()=>{z&&(q({type:Qe.Fetched,payload:z}),Ye(z.database_name))}),[z]),(0,h.useEffect)((()=>{Se&&Ae(!1),ie&&o&&Ha(o)}),[ie]),(0,h.useEffect)((()=>{var e;ea&&(null==(e=document)||e.getElementsByClassName("ant-upload-list-item-name")[0].scrollIntoView())}),[ea]),(0,h.useEffect)((()=>{ra([...Ua])}),[Ua]),(0,h.useEffect)((()=>{oa([...Pa])}),[Pa]),(0,h.useEffect)((()=>{da([...qa])}),[qa]),(0,h.useEffect)((()=>{ha([...Oa])}),[Oa]),(0,h.useEffect)((()=>{var e;void 0!==(null==P||null==(e=P.parameters)?void 0:e.ssh)&&ba(P.parameters.ssh)}),[null==P||null==(T=P.parameters)?void 0:T.ssh]);const Wa=()=>ta?(0,Y.Y)(G,{children:(0,Y.Y)(E.A,{errorMessage:ta,showDbInstallInstructions:la.length>0})}):null,Ga=e=>{var a,t;const n=null!=(a=null==(t=e.currentTarget)?void 0:t.value)?a:"";Re(n.toUpperCase()===(0,d.t)("OVERWRITE"))},Qa=()=>{let e=[];var a;return i()(M)?i()(se)||"GENERIC_DB_ENGINE_ERROR"!==(null==se?void 0:se.error_type)||(e=[(null==se?void 0:se.description)||(null==se?void 0:se.message)]):e="object"==typeof M?Object.values(M):"string"==typeof M?[M]:[],e.length?(0,Y.Y)(We,{children:(0,Y.Y)(N.A,{title:(0,d.t)("Database Creation Error"),description:(0,d.t)('We are unable to connect to your database. Click "See more" for database-provided information that may help troubleshoot the issue.'),descriptionDetails:(null==(a=e)?void 0:a[0])||(null==se?void 0:se.description)})}):(0,Y.Y)(Y.FK,{})},Ja=()=>{Ae(!0),L(null==z?void 0:z.id).then((e=>{(0,p.SO)(p.Hh.Database,e)}))},Xa=()=>(0,Y.Y)(He,{db:P,onSSHTunnelParametersChange:({target:e})=>{Na(Qe.ParametersSSHTunnelChange,{type:e.type,name:e.name,value:e.value}),Ea()},setSSHTunnelLoginMethod:e=>q({type:Qe.SetSSHTunnelLoginMethod,payload:{login_method:e}})}),Za=()=>(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(ke,{isEditMode:xa,db:P,sslForced:!1,dbModel:Fa,onAddTableCatalog:()=>{q({type:Qe.AddTableCatalogSheet})},onQueryChange:({target:e})=>Na(Qe.QueryChange,{name:e.name,value:e.value}),onExtraInputChange:({target:e})=>Na(Qe.ExtraInputChange,{name:e.name,value:e.value}),onEncryptedExtraInputChange:({target:e})=>Na(Qe.EncryptedExtraInputChange,{name:e.name,value:e.value}),onRemoveTableCatalog:e=>{q({type:Qe.RemoveTableCatalogSheet,payload:{indexToDelete:e}})},onParametersChange:ka,onChange:({target:e})=>Na(Qe.TextChange,{name:e.name,value:e.value}),getValidation:()=>ue(P),validationErrors:se,getPlaceholder:Da,clearValidationErrors:Ea}),ga&&(0,Y.Y)(Ge,{children:Xa()})]});if(Ve.length>0&&(Ta.length||la.length||ia.length||sa.length||ca.length))return(0,Y.FD)(v.Ay,{centered:!0,css:e=>[H,K(e),Q(e),J(e)],footer:Ba(),maskClosable:!1,name:"database",onHide:$a,onHandledPrimaryAction:Ra,primaryButtonName:(0,d.t)("Connect"),show:l,title:(0,Y.Y)("h4",{children:(0,d.t)("Connect a database")}),width:"500px",children:[(0,Y.Y)(Ue,{db:P,dbName:xe,dbModel:Fa,fileList:Ve,hasConnectedDb:ve,isEditMode:xa,isLoading:Se,useSqlAlchemyForm:wa}),Ta.length?(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(G,{children:(0,Y.Y)(b.A,{closable:!1,css:e=>(e=>c.AH`
  margin: ${4*e.gridUnit}px 0;

  .antd5-alert-message {
    margin: 0;
  }
`)(e),type:"warning",showIcon:!0,message:"",description:(0,d.t)("You are importing one or more databases that already exist. Overwriting might cause you to lose some of your work. Are you sure you want to overwrite?")})}),(0,Y.Y)(D.A,{id:"confirm_overwrite",name:"confirm_overwrite",required:!0,validationMethods:{onBlur:()=>{}},errorMessage:null==se?void 0:se.confirm_overwrite,label:(0,d.t)('Type "%s" to confirm',(0,d.t)("OVERWRITE")),onChange:Ga,css:B})]}):null,Wa(),la.length||ia.length||sa.length||ca.length?[...new Set([...la,...ia,...sa,...ca])].map((e=>(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(G,{children:(0,Y.Y)(b.A,{closable:!1,css:e=>W(e),type:"info",showIcon:!0,message:"Database passwords",description:(0,d.t)('The passwords for the databases below are needed in order to import them. Please note that the "Secure Extra" and "Certificate" sections of the database configuration are not present in explore files and should be added manually after the import if they are needed.')})}),(null==la?void 0:la.indexOf(e))>=0&&(0,Y.Y)(D.A,{id:"password_needed",name:"password_needed",required:!0,value:Ee[e],onChange:a=>$e({...Ee,[e]:a.target.value}),validationMethods:{onBlur:()=>{}},errorMessage:null==se?void 0:se.password_needed,label:(0,d.t)("%s PASSWORD",e.slice(10)),css:B}),(null==ia?void 0:ia.indexOf(e))>=0&&(0,Y.Y)(D.A,{id:"ssh_tunnel_password_needed",name:"ssh_tunnel_password_needed",required:!0,value:Te[e],onChange:a=>Pe({...Te,[e]:a.target.value}),validationMethods:{onBlur:()=>{}},errorMessage:null==se?void 0:se.ssh_tunnel_password_needed,label:(0,d.t)("%s SSH TUNNEL PASSWORD",e.slice(10)),css:B}),(null==sa?void 0:sa.indexOf(e))>=0&&(0,Y.Y)(D.A,{id:"ssh_tunnel_private_key_needed",name:"ssh_tunnel_private_key_needed",required:!0,value:qe[e],onChange:a=>Oe({...qe,[e]:a.target.value}),validationMethods:{onBlur:()=>{}},errorMessage:null==se?void 0:se.ssh_tunnel_private_key_needed,label:(0,d.t)("%s SSH TUNNEL PRIVATE KEY",e.slice(10)),css:B}),(null==ca?void 0:ca.indexOf(e))>=0&&(0,Y.Y)(D.A,{id:"ssh_tunnel_private_key_password_needed",name:"ssh_tunnel_private_key_password_needed",required:!0,value:ze[e],onChange:a=>Me({...ze,[e]:a.target.value}),validationMethods:{onBlur:()=>{}},errorMessage:null==se?void 0:se.ssh_tunnel_private_key_password_needed,label:(0,d.t)("%s SSH TUNNEL PRIVATE KEY PASSWORD",e.slice(10)),css:B})]}))):null]});const et=xa?(e=>(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(ce,{onClick:$a,children:(0,d.t)("Close")},"close"),(0,Y.Y)(ce,{buttonStyle:"primary",onClick:Ra,disabled:null==e?void 0:e.is_managed_externally,loading:Se,tooltip:null!=e&&e.is_managed_externally?(0,d.t)("This database is managed externally, and can't be edited in Superset"):"",children:(0,d.t)("Finish")},"submit")]}))(P):Ba();return Ca?(0,Y.FD)(v.Ay,{css:e=>[R,H,K(e),Q(e),J(e)],name:"database",onHandledPrimaryAction:Ra,onHide:$a,primaryButtonName:xa?(0,d.t)("Save"):(0,d.t)("Connect"),width:"500px",centered:!0,show:l,title:(0,Y.FD)("h4",{children:[xa?(0,Y.Y)(x.F.EditOutlined,{iconSize:"l",css:c.AH`
                margin: auto ${2*U.gridUnit}px auto 0;
              `}):(0,Y.Y)(x.F.InsertRowAboveOutlined,{iconSize:"l",css:c.AH`
                margin: auto ${2*U.gridUnit}px auto 0;
              `}),xa?(0,d.t)("Edit database"):(0,d.t)("Connect a database")]}),footer:et,maskClosable:!1,children:[(0,Y.Y)(he,{children:(0,Y.Y)(re,{children:(0,Y.Y)(Ue,{isLoading:Se,isEditMode:xa,useSqlAlchemyForm:wa,hasConnectedDb:ve,db:P,dbName:xe,dbModel:Fa})})}),(0,Y.FD)(Ke,{defaultActiveKey:"1",activeKey:ee,onTabClick:e=>ae(e),animated:{inkBar:!0,tabPane:!0},children:[(0,Y.FD)(m.Ay.TabPane,{tab:(0,Y.Y)("span",{children:(0,d.t)("Basic")}),children:[wa?(0,Y.FD)(te,{children:[(0,Y.FD)(be,{db:P,onInputChange:({target:e})=>Na(Qe.InputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),conf:fa,testConnection:()=>{var t;if(null==P||!P.sqlalchemy_uri)return void e((0,d.t)("Please enter a SQLAlchemy URI to test"));const n={sqlalchemy_uri:(null==P?void 0:P.sqlalchemy_uri)||"",database_name:(null==P||null==(t=P.database_name)?void 0:t.trim())||void 0,impersonate_user:(null==P?void 0:P.impersonate_user)||void 0,extra:null==P?void 0:P.extra,masked_encrypted_extra:(null==P?void 0:P.masked_encrypted_extra)||"",server_cert:(null==P?void 0:P.server_cert)||void 0,ssh_tunnel:!i()(null==P?void 0:P.ssh_tunnel)&&ga?{...P.ssh_tunnel,server_port:Number(P.ssh_tunnel.server_port)}:void 0};Ne(!0),(0,k.ym)(n,(a=>{Ne(!1),e(a)}),(e=>{Ne(!1),a(e)}))},testInProgress:De,children:[(0,Y.Y)(ma,{dbModel:Fa,db:P,changeMethods:{onParametersChange:ka},clearValidationErrors:Ea}),ga&&Xa()]}),(lt=(null==P?void 0:P.backend)||(null==P?void 0:P.engine),void 0!==(null==ie||null==(rt=ie.databases)||null==(it=rt.find((e=>e.backend===lt||e.engine===lt)))?void 0:it.parameters)&&!xa&&(0,Y.FD)("div",{css:e=>j(e),children:[(0,Y.Y)(f.A,{buttonStyle:"link",onClick:()=>q({type:Qe.ConfigMethodChange,payload:{database_name:null==P?void 0:P.database_name,configuration_method:C.DynamicForm,engine:null==P?void 0:P.engine}}),css:e=>(e=>c.AH`
  font-weight: ${e.typography.weights.normal};
  text-transform: initial;
  padding: ${8*e.gridUnit}px 0 0;
  margin-left: 0px;
`)(e),children:(0,d.t)("Connect this database using the dynamic form instead")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Click this link to switch to an alternate form that exposes only the required fields needed to connect this database."),viewBox:"0 -6 24 24"})]}))]}):Za(),!xa&&(0,Y.Y)(G,{children:(0,Y.Y)(b.A,{closable:!1,css:e=>W(e),message:(0,d.t)("Additional fields may be required"),showIcon:!0,description:(0,Y.FD)(Y.FK,{children:[(0,d.t)("Select databases require additional fields to be completed in the Advanced tab to successfully connect the database. Learn what requirements your databases has "),(0,Y.Y)("a",{href:Ie,target:"_blank",rel:"noopener noreferrer",className:"additional-fields-alert-description",children:(0,d.t)("here")}),"."]}),type:"info"})}),Sa&&Qa()]},"1"),(0,Y.Y)(m.Ay.TabPane,{tab:(0,Y.Y)("span",{children:(0,d.t)("Advanced")}),children:(0,Y.Y)(me,{extraExtension:va,db:P,onInputChange:({target:e})=>Na(Qe.InputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onTextChange:({target:e})=>Na(Qe.TextChange,{name:e.name,value:e.value}),onEditorChange:e=>Na(Qe.EditorChange,e),onExtraInputChange:({target:e})=>{Na(Qe.ExtraInputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value})},onExtraEditorChange:e=>{Na(Qe.ExtraEditorChange,e)}})},"2")]})]}):(0,Y.FD)(v.Ay,{css:e=>[H,K(e),Q(e),J(e)],name:"database",onHandledPrimaryAction:Ra,onHide:$a,primaryButtonName:ve?(0,d.t)("Finish"):(0,d.t)("Connect"),width:"500px",centered:!0,show:l,title:(0,Y.FD)("h4",{children:[(0,Y.Y)(x.F.InsertRowAboveOutlined,{iconSize:"l",css:c.AH`
              margin: auto ${2*U.gridUnit}px auto 0;
            `}),(0,d.t)("Connect a database")]}),footer:Ba(),maskClosable:!1,children:[!Se&&ve?(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(Ue,{isLoading:Se,isEditMode:xa,useSqlAlchemyForm:wa,hasConnectedDb:ve,db:P,dbName:xe,dbModel:Fa,editNewDb:we}),ye&&(0,Y.FD)(Xe,{children:[(0,Y.Y)(f.A,{buttonStyle:"secondary",onClick:()=>{Ae(!0),Ja(),Ia("/dataset/add/")},children:(0,d.t)("CREATE DATASET")}),(0,Y.Y)(f.A,{buttonStyle:"secondary",onClick:()=>{Ae(!0),Ja(),Ia("/sqllab?db=true")},children:(0,d.t)("QUERY DATA IN SQL LAB")})]}),we?Za():(0,Y.Y)(me,{extraExtension:va,db:P,onInputChange:({target:e})=>Na(Qe.InputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onTextChange:({target:e})=>Na(Qe.TextChange,{name:e.name,value:e.value}),onEditorChange:e=>Na(Qe.EditorChange,e),onExtraInputChange:({target:e})=>{Na(Qe.ExtraInputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value})},onExtraEditorChange:e=>Na(Qe.ExtraEditorChange,e)})]}):(0,Y.Y)(Y.FK,{children:!Se&&(P?(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(Ue,{isLoading:Se,isEditMode:xa,useSqlAlchemyForm:wa,hasConnectedDb:ve,db:P,dbName:xe,dbModel:Fa}),Ya&&(()=>{var e,a,t,n,l;const{hostname:r}=window.location;let i=(null==_a||null==(e=_a.REGIONAL_IPS)?void 0:e.default)||"";const o=(null==_a?void 0:_a.REGIONAL_IPS)||{};return Object.entries(o).forEach((([e,a])=>{const t=new RegExp(e);r.match(t)&&(i=a)})),(null==P?void 0:P.engine)&&(0,Y.Y)(G,{children:(0,Y.Y)(b.A,{closable:!1,css:e=>W(e),type:"info",showIcon:!0,message:(null==(a=Be[P.engine])?void 0:a.message)||(null==_a||null==(t=_a.DEFAULT)?void 0:t.message),description:(null==(n=Be[P.engine])?void 0:n.description)||(null==_a||null==(l=_a.DEFAULT)?void 0:l.description)+i})})})(),Za(),(0,Y.Y)("div",{css:e=>j(e),children:Fa.engine!==S.GSheet&&(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(f.A,{buttonStyle:"link",onClick:()=>q({type:Qe.ConfigMethodChange,payload:{engine:P.engine,configuration_method:C.SqlalchemyUri,database_name:P.database_name}}),css:ne,children:(0,d.t)("Connect this database with a SQLAlchemy URI string instead")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Click this link to switch to an alternate form that allows you to input the SQLAlchemy URL for this database manually."),viewBox:"0 -6 24 24"})]})}),Sa&&Qa()]}):(0,Y.FD)(de,{children:[(0,Y.Y)(Ue,{isLoading:Se,isEditMode:xa,useSqlAlchemyForm:wa,hasConnectedDb:ve,db:P,dbName:xe,dbModel:Fa}),(0,Y.Y)("div",{className:"preferred",children:null==ie||null==(nt=ie.databases)?void 0:nt.filter((e=>e.preferred)).map((e=>(0,Y.Y)(w,{className:"preferred-item",onClick:()=>Ha(e.name),buttonText:e.name,icon:null==ya?void 0:ya[e.engine]},`${e.name}`)))}),(0,Y.FD)("div",{className:"available",children:[(0,Y.Y)("h4",{className:"available-label",children:(0,d.t)("Or choose from a list of other databases we support:")}),(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("Supported databases")}),(0,Y.FD)(g._P,{className:"available-select",onChange:Ha,placeholder:(0,d.t)("Choose a database..."),showSearch:!0,children:[null==(at=[...(null==ie?void 0:ie.databases)||[]])?void 0:at.sort(((e,a)=>e.name.localeCompare(a.name))).map(((e,a)=>(0,Y.Y)(g._P.Option,{value:e.name,children:e.name},`database-${a}`))),(0,Y.Y)(g._P.Option,{value:"Other",children:(0,d.t)("Other")},"Other")]}),(0,Y.Y)(b.A,{showIcon:!0,closable:!1,css:e=>W(e),type:"info",message:(null==_a||null==(tt=_a.ADD_DATABASE)?void 0:tt.message)||(0,d.t)("Want to add a new database?"),description:null!=_a&&_a.ADD_DATABASE?(0,Y.FD)(Y.FK,{children:[(0,d.t)("Any databases that allow connections via SQL Alchemy URIs can be added. "),(0,Y.Y)("a",{href:null==_a?void 0:_a.ADD_DATABASE.contact_link,target:"_blank",rel:"noopener noreferrer",children:null==_a?void 0:_a.ADD_DATABASE.contact_description_link})," ",null==_a?void 0:_a.ADD_DATABASE.description]}):(0,Y.FD)(Y.FK,{children:[(0,d.t)("Any databases that allow connections via SQL Alchemy URIs can be added. Learn about how to connect a database driver "),(0,Y.Y)("a",{href:Ie,target:"_blank",rel:"noopener noreferrer",children:(0,d.t)("here")}),"."]})})]}),(0,Y.Y)(pe,{children:(0,Y.Y)(g._O,{name:"databaseFile",id:"databaseFile",accept:".yaml,.json,.yml,.zip",customRequest:()=>{},onChange:async e=>{na(""),ra([]),oa([]),da([]),ha([]),$e({}),Pe({}),Oe({}),Me({}),aa(!0),Je([{...e.file,status:"done"}]),e.file.originFileObj instanceof File&&await La(e.file.originFileObj,Ee,Te,qe,ze,Le)&&(null==t||t())},onRemove:e=>(Je(Ve.filter((a=>a.uid!==e.uid))),!1),children:(0,Y.Y)(f.A,{buttonStyle:"link",type:"link",css:le,children:(0,d.t)("Import database from file")})})}),Wa()]}))}),Se&&(0,Y.Y)(I.A,{})]});var at,tt,nt,lt,rt,it}))},62221:(e,a,t)=>{var n;function l(e,a){try{const t=localStorage.getItem(e);return null===t?a:JSON.parse(t)}catch{return a}}function r(e,a){try{localStorage.setItem(e,JSON.stringify(a))}catch{}}function i(e,a){return l(e,a)}function o(e,a){r(e,a)}t.d(a,{Gq:()=>i,Hh:()=>n,SO:()=>o,SX:()=>l,Wr:()=>r}),function(e){e.Database="db",e.ChartSplitSizes="chart_split_sizes",e.ControlsWidth="controls_width",e.DatasourceWidth="datasource_width",e.IsDatapanelOpen="is_datapanel_open",e.HomepageChartFilter="homepage_chart_filter",e.HomepageDashboardFilter="homepage_dashboard_filter",e.HomepageCollapseState="homepage_collapse_state",e.HomepageActivityFilter="homepage_activity_filter",e.DatasetnameSetSuccessful="datasetname_set_successful",e.SqllabIsAutocompleteEnabled="sqllab__is_autocomplete_enabled",e.SqllabIsRenderHtmlEnabled="sqllab__is_render_html_enabled",e.ExploreDataTableOriginalFormattedTimeColumns="explore__data_table_original_formatted_time_columns",e.DashboardCustomFilterBarWidths="dashboard__custom_filter_bar_widths",e.DashboardExploreContext="dashboard__explore_context",e.DashboardEditorShowOnlyMyCharts="dashboard__editor_show_only_my_charts",e.CommonResizableSidebarWidths="common__resizable_sidebar_widths"}(n||(n={}))},76479:(e,a,t)=>{t.d(a,{A:()=>Y});var n,l=t(58168),r=t(23029),i=t(92901),o=t(85501),s=t(29426),d=t(96540),c=t(89379),h=t(64467),u=t(26076),p=t(42234),m=t(46942),g=t.n(m),b=["letter-spacing","line-height","padding-top","padding-bottom","font-family","font-weight","font-size","font-variant","text-rendering","text-transform","width","text-indent","padding-left","padding-right","border-width","box-sizing","word-break"],v={};var f,y=t(2833),_=t.n(y);!function(e){e[e.NONE=0]="NONE",e[e.RESIZING=1]="RESIZING",e[e.RESIZED=2]="RESIZED"}(f||(f={}));const x=function(e){(0,o.A)(t,e);var a=(0,s.A)(t);function t(e){var i;return(0,r.A)(this,t),(i=a.call(this,e)).nextFrameActionId=void 0,i.resizeFrameId=void 0,i.textArea=void 0,i.saveTextArea=function(e){i.textArea=e},i.handleResize=function(e){var a=i.state.resizeStatus,t=i.props,n=t.autoSize,l=t.onResize;a===f.NONE&&("function"==typeof l&&l(e),n&&i.resizeOnNextFrame())},i.resizeOnNextFrame=function(){cancelAnimationFrame(i.nextFrameActionId),i.nextFrameActionId=requestAnimationFrame(i.resizeTextarea)},i.resizeTextarea=function(){var e=i.props.autoSize;if(e&&i.textArea){var a=e.minRows,t=e.maxRows,l=function(e){var a=arguments.length>1&&void 0!==arguments[1]&&arguments[1],t=arguments.length>2&&void 0!==arguments[2]?arguments[2]:null,l=arguments.length>3&&void 0!==arguments[3]?arguments[3]:null;n||((n=document.createElement("textarea")).setAttribute("tab-index","-1"),n.setAttribute("aria-hidden","true"),document.body.appendChild(n)),e.getAttribute("wrap")?n.setAttribute("wrap",e.getAttribute("wrap")):n.removeAttribute("wrap");var r=function(e){var a=arguments.length>1&&void 0!==arguments[1]&&arguments[1],t=e.getAttribute("id")||e.getAttribute("data-reactid")||e.getAttribute("name");if(a&&v[t])return v[t];var n=window.getComputedStyle(e),l=n.getPropertyValue("box-sizing")||n.getPropertyValue("-moz-box-sizing")||n.getPropertyValue("-webkit-box-sizing"),r=parseFloat(n.getPropertyValue("padding-bottom"))+parseFloat(n.getPropertyValue("padding-top")),i=parseFloat(n.getPropertyValue("border-bottom-width"))+parseFloat(n.getPropertyValue("border-top-width")),o={sizingStyle:b.map((function(e){return"".concat(e,":").concat(n.getPropertyValue(e))})).join(";"),paddingSize:r,borderSize:i,boxSizing:l};return a&&t&&(v[t]=o),o}(e,a),i=r.paddingSize,o=r.borderSize,s=r.boxSizing,d=r.sizingStyle;n.setAttribute("style","".concat(d,";").concat("\n  min-height:0 !important;\n  max-height:none !important;\n  height:0 !important;\n  visibility:hidden !important;\n  overflow:hidden !important;\n  position:absolute !important;\n  z-index:-1000 !important;\n  top:0 !important;\n  right:0 !important\n")),n.value=e.value||e.placeholder||"";var c,h=Number.MIN_SAFE_INTEGER,u=Number.MAX_SAFE_INTEGER,p=n.scrollHeight;if("border-box"===s?p+=o:"content-box"===s&&(p-=i),null!==t||null!==l){n.value=" ";var m=n.scrollHeight-i;null!==t&&(h=m*t,"border-box"===s&&(h=h+i+o),p=Math.max(h,p)),null!==l&&(u=m*l,"border-box"===s&&(u=u+i+o),c=p>u?"":"hidden",p=Math.min(u,p))}return{height:p,minHeight:h,maxHeight:u,overflowY:c,resize:"none"}}(i.textArea,!1,a,t);i.setState({textareaStyles:l,resizeStatus:f.RESIZING},(function(){cancelAnimationFrame(i.resizeFrameId),i.resizeFrameId=requestAnimationFrame((function(){i.setState({resizeStatus:f.RESIZED},(function(){i.resizeFrameId=requestAnimationFrame((function(){i.setState({resizeStatus:f.NONE}),i.fixFirefoxAutoScroll()}))}))}))}))}},i.renderTextArea=function(){var e=i.props,a=e.prefixCls,t=void 0===a?"rc-textarea":a,n=e.autoSize,r=e.onResize,o=e.className,s=e.disabled,m=i.state,b=m.textareaStyles,v=m.resizeStatus,y=(0,p.A)(i.props,["prefixCls","onPressEnter","autoSize","defaultValue","onResize"]),_=g()(t,o,(0,h.A)({},"".concat(t,"-disabled"),s));"value"in y&&(y.value=y.value||"");var x=(0,c.A)((0,c.A)((0,c.A)({},i.props.style),b),v===f.RESIZING?{overflowX:"hidden",overflowY:"hidden"}:null);return d.createElement(u.default,{onResize:i.handleResize,disabled:!(n||r)},d.createElement("textarea",(0,l.A)({},y,{className:_,style:x,ref:i.saveTextArea})))},i.state={textareaStyles:{},resizeStatus:f.NONE},i}return(0,i.A)(t,[{key:"componentDidUpdate",value:function(e){e.value===this.props.value&&_()(e.autoSize,this.props.autoSize)||this.resizeTextarea()}},{key:"componentWillUnmount",value:function(){cancelAnimationFrame(this.nextFrameActionId),cancelAnimationFrame(this.resizeFrameId)}},{key:"fixFirefoxAutoScroll",value:function(){try{if(document.activeElement===this.textArea){var e=this.textArea.selectionStart,a=this.textArea.selectionEnd;this.textArea.setSelectionRange(e,a)}}catch(e){}}},{key:"render",value:function(){return this.renderTextArea()}}]),t}(d.Component),Y=function(e){(0,o.A)(t,e);var a=(0,s.A)(t);function t(e){var n;(0,r.A)(this,t),(n=a.call(this,e)).resizableTextArea=void 0,n.focus=function(){n.resizableTextArea.textArea.focus()},n.saveTextArea=function(e){n.resizableTextArea=e},n.handleChange=function(e){var a=n.props.onChange;n.setValue(e.target.value,(function(){n.resizableTextArea.resizeTextarea()})),a&&a(e)},n.handleKeyDown=function(e){var a=n.props,t=a.onPressEnter,l=a.onKeyDown;13===e.keyCode&&t&&t(e),l&&l(e)};var l=void 0===e.value||null===e.value?e.defaultValue:e.value;return n.state={value:l},n}return(0,i.A)(t,[{key:"setValue",value:function(e,a){"value"in this.props||this.setState({value:e},a)}},{key:"blur",value:function(){this.resizableTextArea.textArea.blur()}},{key:"render",value:function(){return d.createElement(x,(0,l.A)({},this.props,{value:this.state.value,onKeyDown:this.handleKeyDown,onChange:this.handleChange,ref:this.saveTextArea}))}}],[{key:"getDerivedStateFromProps",value:function(e){return"value"in e?{value:e.value}:null}}]),t}(d.Component)},82741:(e,a,t)=>{t.d(a,{A:()=>se});var n=t(38221),l=t.n(n),r=t(96540),i=t(96453),o=t(17437),s=t(32132),d=t(15595),c=t(6749),h=t(19129),u=t(61574),p=t(71519),m=t(78532),g=t(67073),b=t(35837),v=t(27023),f=t(62193),y=t.n(f),_=t(58156),x=t.n(_),Y=t(58561),w=t.n(Y),C=t(61225),S=t(33231),A=t(72391),F=t(78518),D=t(35742),N=t(35768),E=t(83188),k=t(84666),$=t(65256),I=t(43293),T=t(19980),U=t(30703),P=t(2445);const q=({version:e="unknownVersion",sha:a="unknownSHA",build:t="unknownBuild"})=>{const n=`https://apachesuperset.gateway.scarf.sh/pixel/0d3461e1-abb1-4691-a0aa-5ed50de66af0/${e}/${a}/${t}`;return(0,P.Y)("img",{referrerPolicy:"no-referrer-when-downgrade",src:n,width:0,height:0,alt:""})},{SubMenu:O}=c.NG,z=i.I4.div`
  display: flex;
  align-items: center;

  & i {
    margin-right: ${({theme:e})=>2*e.gridUnit}px;
  }

  & a {
    display: block;
    width: 150px;
    word-wrap: break-word;
    text-decoration: none;
  }
`,M=i.I4.i`
  margin-top: 2px;
`;function L(e){const{locale:a,languages:t,...n}=e,l=(0,i.DP)();return(0,P.Y)(O,{css:o.AH`
        [data-icon='caret-down'] {
          color: ${l.colors.grayscale.base};
          font-size: ${l.typography.sizes.xxs}px;
          margin-left: ${l.gridUnit}px;
        }
      `,"aria-label":"Languages",title:(0,P.Y)("div",{className:"f16",children:(0,P.Y)(M,{className:`flag ${t[a].flag}`})}),icon:(0,P.Y)(g.F.CaretDownOutlined,{iconSize:"xs"}),...n,children:Object.keys(t).map((e=>(0,P.Y)(c.NG.Item,{style:{whiteSpace:"normal",height:"auto"},children:(0,P.FD)(z,{className:"f16",children:[(0,P.Y)("i",{className:`flag ${t[e].flag}`}),(0,P.Y)("a",{href:t[e].url,children:t[e].name})]})},e)))})}var R=t(3139);const H=(0,A.a)(),j=e=>o.AH`
  padding: ${1.5*e.gridUnit}px ${4*e.gridUnit}px
    ${4*e.gridUnit}px ${7*e.gridUnit}px;
  color: ${e.colors.grayscale.base};
  font-size: ${e.typography.sizes.xs}px;
  white-space: nowrap;
`,V=e=>o.AH`
  color: ${e.colors.grayscale.light1};
`,B=i.I4.div`
  display: flex;
  height: 100%;
  flex-direction: row;
  justify-content: ${({align:e})=>e};
  align-items: center;
  margin-right: ${({theme:e})=>e.gridUnit}px;
`,K=i.I4.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
`,W=i.I4.a`
  padding-right: ${({theme:e})=>e.gridUnit}px;
  padding-left: ${({theme:e})=>e.gridUnit}px;
`,G=e=>o.AH`
  color: ${e.colors.grayscale.light5};
`,Q=e=>o.AH`
  &:hover {
    color: ${e.colors.primary.base} !important;
    cursor: pointer !important;
  }
`,{SubMenu:J}=c.W1,X=(0,i.I4)(J)`
  ${({theme:e})=>o.AH`
    [data-icon='caret-down'] {
      color: ${e.colors.grayscale.base};
      font-size: ${e.typography.sizes.xxs}px;
      margin-left: ${e.gridUnit}px;
    }
    &.antd5-menu-submenu-active {
      .antd5-menu-title-content {
        color: ${e.colors.primary.base};
      }
    }
  `}
`,Z=({align:e,settings:a,navbarRight:t,isFrontendRoute:n,environmentTag:l,setQuery:s})=>{const d=(0,C.d4)((e=>e.user)),u=(0,C.d4)((e=>{var a;return null==(a=e.dashboardInfo)?void 0:a.id})),m=d||{},{roles:b}=m,{CSV_EXTENSIONS:v,COLUMNAR_EXTENSIONS:f,EXCEL_EXTENSIONS:_,ALLOWED_EXTENSIONS:Y,HAS_GSHEETS_INSTALLED:S}=(0,C.d4)((e=>e.common.conf)),[A,O]=(0,r.useState)(!1),[z,M]=(0,r.useState)(!1),[J,Z]=(0,r.useState)(!1),[ee,ae]=(0,r.useState)(!1),[te,ne]=(0,r.useState)(""),le=(0,k.L)("can_sqllab","Superset",b),re=(0,k.L)("can_write","Dashboard",b),ie=(0,k.L)("can_write","Chart",b),oe=(0,k.L)("can_write","Database",b),se=(0,k.L)("can_write","Dataset",b),{canUploadData:de,canUploadCSV:ce,canUploadColumnar:he,canUploadExcel:ue}=(0,U.c8)(b,v,f,_,Y),pe=le||ie||re,[me,ge]=(0,r.useState)(!1),[be,ve]=(0,r.useState)(!1),fe=(0,$.N6)(d),ye=me||fe,_e=[{label:(0,F.t)("Data"),icon:"fa-database",childs:[{label:(0,F.t)("Connect database"),name:R.$.DbConnection,perm:oe&&!be},{label:(0,F.t)("Create dataset"),name:R.$.DatasetCreation,url:"/dataset/add/",perm:se&&be},{label:(0,F.t)("Connect Google Sheet"),name:R.$.GoogleSheets,perm:oe&&S},{label:(0,F.t)("Upload CSV to database"),name:R.$.CSVUpload,perm:ce&&ye,disable:fe&&!me},{label:(0,F.t)("Upload Excel to database"),name:R.$.ExcelUpload,perm:ue&&ye,disable:fe&&!me},{label:(0,F.t)("Upload Columnar file to database"),name:R.$.ColumnarUpload,perm:he&&ye,disable:fe&&!me}]},{label:(0,F.t)("SQL query"),url:"/sqllab?new=true",icon:"fa-fw fa-search",perm:"can_sqllab",view:"Superset"},{label:(0,F.t)("Chart"),url:Number.isInteger(u)?`/chart/add?dashboard_id=${u}`:"/chart/add",icon:"fa-fw fa-bar-chart",perm:"can_write",view:"Chart"},{label:(0,F.t)("Dashboard"),url:"/dashboard/new",icon:"fa-fw fa-dashboard",perm:"can_write",view:"Dashboard"}],xe=()=>{D.A.get({endpoint:`/api/v1/database/?q=${w().encode({filters:[{col:"allow_file_upload",opr:"upload_is_enabled",value:!0}]})}`}).then((({json:e})=>{var a;const t=(null==e||null==(a=e.result)?void 0:a.filter((e=>{var a;return null==e||null==(a=e.engine_information)?void 0:a.supports_file_upload})))||[];ge((null==t?void 0:t.length)>=1)}))},Ye=()=>{D.A.get({endpoint:`/api/v1/database/?q=${w().encode({filters:[{col:"database_name",opr:"neq",value:"examples"}]})}`}).then((({json:e})=>{ve(e.count>=1)}))};(0,r.useEffect)((()=>{de&&xe()}),[de]),(0,r.useEffect)((()=>{(oe||se)&&Ye()}),[oe,se]);const we=e=>(0,P.Y)("i",{className:`fa ${e.icon}`}),Ce=(0,F.t)("Enable 'Allow file uploads to database' in any database's settings"),Se=e=>e.disable?(0,P.Y)(c.W1.Item,{css:V,disabled:!0,children:(0,P.Y)(h.m_,{placement:"top",title:Ce,children:e.label})},e.name):(0,P.Y)(c.W1.Item,{css:Q,children:e.url?(0,P.FD)("a",{href:(0,E.A)(e.url),children:[" ",e.label," "]}):e.label},e.name),Ae=H.get("navbar.right"),Fe=H.get("navbar.right-menu.item.icon"),De=(0,i.DP)();return(0,P.FD)(B,{align:e,children:[oe&&(0,P.Y)(I.Ay,{onHide:()=>{ne(""),O(!1)},show:A,dbEngine:te,onDatabaseAdd:()=>s({databaseAdded:!0})}),ce&&(0,P.Y)(T.A,{onHide:()=>M(!1),show:z,allowedExtensions:v,type:"csv"}),ue&&(0,P.Y)(T.A,{onHide:()=>Z(!1),show:J,allowedExtensions:_,type:"excel"}),he&&(0,P.Y)(T.A,{onHide:()=>ae(!1),show:ee,allowedExtensions:f,type:"columnar"}),(null==l?void 0:l.text)&&(0,P.Y)(N.Ay,{css:(0,o.AH)({borderRadius:125*De.gridUnit+"px"},"",""),color:/^#(?:[0-9a-f]{3}){1,2}$/i.test(l.color)?l.color:x()(De.colors,l.color),children:(0,P.Y)("span",{css:G,children:l.text})}),(0,P.FD)(c.W1,{css:o.AH`
          display: flex;
          flex-direction: row;
        `,selectable:!1,mode:"horizontal",onClick:e=>{e.key===R.$.DbConnection?O(!0):e.key===R.$.GoogleSheets?(O(!0),ne("Google Sheets")):e.key===R.$.CSVUpload?M(!0):e.key===R.$.ExcelUpload?Z(!0):e.key===R.$.ColumnarUpload&&ae(!0)},onOpenChange:e=>(e.length>1&&!y()(null==e?void 0:e.filter((e=>{var a;return e.includes(`sub2_${null==_e||null==(a=_e[0])?void 0:a.label}`)})))&&(de&&xe(),(oe||se)&&Ye()),null),disabledOverflow:!0,children:[Ae&&(0,P.Y)(Ae,{}),!t.user_is_anonymous&&pe&&(0,P.Y)(X,{title:(0,P.Y)(g.F.PlusOutlined,{iconColor:De.colors.primary.dark1}),icon:(0,P.Y)(g.F.CaretDownOutlined,{iconSize:"xs"}),children:null==_e||null==_e.map?void 0:_e.map((e=>{var a;const t=null==(a=e.childs)?void 0:a.some((e=>"object"==typeof e&&!!e.perm));if(e.childs){var l;if(t)return(0,P.Y)(X,{className:"data-menu",title:e.label,icon:we(e),children:null==e||null==(l=e.childs)||null==l.map?void 0:l.map(((e,a)=>"string"!=typeof e&&e.name&&e.perm?(0,P.FD)(r.Fragment,{children:[3===a&&(0,P.Y)(c.W1.Divider,{}),Se(e)]},e.name):null))},`sub2_${e.label}`);if(!e.url)return null}return(0,k.L)(e.perm,e.view,b)&&(0,P.Y)(c.W1.Item,{children:n(e.url)?(0,P.FD)(p.N_,{to:e.url||"",children:[(0,P.Y)("i",{className:`fa ${e.icon}`})," ",e.label]}):(0,P.FD)("a",{href:(0,E.A)(e.url||""),children:[(0,P.Y)("i",{className:`fa ${e.icon}`})," ",e.label]})},e.label)}))},"sub1"),(0,P.FD)(X,{title:(0,F.t)("Settings"),icon:(0,P.Y)(g.F.CaretDownOutlined,{iconSize:"xs"}),children:[null==a||null==a.map?void 0:a.map(((e,t)=>{var l;return[(0,P.Y)(c.W1.ItemGroup,{title:e.label,children:null==e||null==(l=e.childs)||null==l.map?void 0:l.map((e=>{if("string"!=typeof e){const a=Fe?(0,P.FD)(K,{children:[e.label,(0,P.Y)(Fe,{menuChild:e})]}):e.label;return(0,P.Y)(c.W1.Item,{children:n(e.url)?(0,P.Y)(p.N_,{to:e.url||"",children:a}):(0,P.Y)("a",{href:e.url||"",children:a})},`${e.label}`)}return null}))},`${e.label}`),t<a.length-1&&(0,P.Y)(c.W1.Divider,{},`divider_${t}`)]})),!t.user_is_anonymous&&[(0,P.Y)(c.W1.Divider,{},"user-divider"),(0,P.FD)(c.W1.ItemGroup,{title:(0,F.t)("User"),children:[t.user_info_url&&(0,P.Y)(c.W1.Item,{children:(0,P.Y)("a",{href:t.user_info_url,children:(0,F.t)("Info")})},"info"),(0,P.Y)(c.W1.Item,{onClick:()=>{localStorage.removeItem("redux")},children:(0,P.Y)("a",{href:t.user_logout_url,children:(0,F.t)("Logout")})},"logout")]},"user-section")],(t.version_string||t.version_sha)&&[(0,P.Y)(c.W1.Divider,{},"version-info-divider"),(0,P.Y)(c.W1.ItemGroup,{title:(0,F.t)("About"),children:(0,P.FD)("div",{className:"about-section",children:[t.show_watermark&&(0,P.Y)("div",{css:j,children:(0,F.t)("Powered by Apache Superset")}),t.version_string&&(0,P.FD)("div",{css:j,children:[(0,F.t)("Version"),": ",t.version_string]}),t.version_sha&&(0,P.FD)("div",{css:j,children:[(0,F.t)("SHA"),": ",t.version_sha]}),t.build_number&&(0,P.FD)("div",{css:j,children:[(0,F.t)("Build"),": ",t.build_number]})]})},"about-section")]]},"sub3_settings"),t.show_language_picker&&(0,P.Y)(L,{locale:t.locale,languages:t.languages})]}),t.documentation_url&&(0,P.FD)(P.FK,{children:[(0,P.Y)(W,{href:t.documentation_url,target:"_blank",rel:"noreferrer",title:t.documentation_text||(0,F.t)("Documentation"),children:t.documentation_icon?(0,P.Y)("i",{className:t.documentation_icon}):(0,P.Y)("i",{className:"fa fa-question"})}),(0,P.Y)("span",{children:" "})]}),t.bug_report_url&&(0,P.FD)(P.FK,{children:[(0,P.Y)(W,{href:t.bug_report_url,target:"_blank",rel:"noreferrer",title:t.bug_report_text||(0,F.t)("Report a bug"),children:t.bug_report_icon?(0,P.Y)("i",{className:t.bug_report_icon}):(0,P.Y)("i",{className:"fa fa-bug"})}),(0,P.Y)("span",{children:" "})]}),t.user_is_anonymous&&(0,P.FD)(W,{href:t.user_login_url,children:[(0,P.Y)("i",{className:"fa fa-fw fa-sign-in"}),(0,F.t)("Login")]}),(0,P.Y)(q,{version:t.version_string,sha:t.version_sha,build:t.build_number})]})},ee=e=>{const[,a]=(0,S.sq)({databaseAdded:S.sJ,datasetAdded:S.sJ});return(0,P.Y)(Z,{setQuery:a,...e})};class ae extends r.PureComponent{constructor(...e){super(...e),this.state={hasError:!1},this.noop=()=>{}}static getDerivedStateFromError(){return{hasError:!0}}render(){return this.state.hasError?(0,P.Y)(Z,{setQuery:this.noop,...this.props}):this.props.children}}const te=e=>(0,P.Y)(ae,{...e,children:(0,P.Y)(ee,{...e})}),ne=i.I4.header`
  ${({theme:e})=>`\n      background-color: ${e.colors.grayscale.light5};\n      margin-bottom: 2px;\n      z-index: 10;\n\n      &:nth-last-of-type(2) nav {\n        margin-bottom: 2px;\n      }\n      .caret {\n        display: none;\n      }\n      .navbar-brand {\n        display: flex;\n        flex-direction: column;\n        justify-content: center;\n        /* must be exactly the height of the Antd navbar */\n        min-height: 50px;\n        padding: ${e.gridUnit}px\n          ${2*e.gridUnit}px\n          ${e.gridUnit}px\n          ${4*e.gridUnit}px;\n        max-width: ${e.gridUnit*e.brandIconMaxWidth}px;\n        img {\n          height: 100%;\n          object-fit: contain;\n        }\n        &:focus {\n          border-color: transparent;\n        }\n        &:focus-visible {\n          border-color: ${e.colors.primary.dark1};\n        }\n      }\n      .navbar-brand-text {\n        border-left: 1px solid ${e.colors.grayscale.light2};\n        border-right: 1px solid ${e.colors.grayscale.light2};\n        height: 100%;\n        color: ${e.colors.grayscale.dark1};\n        padding-left: ${4*e.gridUnit}px;\n        padding-right: ${4*e.gridUnit}px;\n        margin-right: ${6*e.gridUnit}px;\n        font-size: ${4*e.gridUnit}px;\n        float: left;\n        display: flex;\n        flex-direction: column;\n        justify-content: center;\n\n        span {\n          max-width: ${58*e.gridUnit}px;\n          white-space: nowrap;\n          overflow: hidden;\n          text-overflow: ellipsis;\n        }\n        @media (max-width: 1127px) {\n          display: none;\n        }\n      }\n      @media (max-width: 767px) {\n        .navbar-brand {\n          float: none;\n        }\n      }\n      @media (max-width: 767px) {\n        .antd5-menu-item {\n          padding: 0 ${6*e.gridUnit}px 0\n            ${3*e.gridUnit}px !important;\n        }\n        .antd5-menu > .antd5-menu-item > span > a {\n          padding: 0px;\n        }\n        .main-nav .antd5-menu-submenu-title > svg:nth-of-type(1) {\n          display: none;\n        }\n      }\n  `}
`,{SubMenu:le}=c.NG,re=(0,i.I4)(le)`
  ${({theme:e})=>o.AH`
    [data-icon="caret-down"] {
      color: ${e.colors.grayscale.base};
      font-size: ${e.typography.sizes.xs}px;
      margin-left: ${e.gridUnit}px;
    }
    &.antd5-menu-submenu {
        padding: ${2*e.gridUnit}px ${4*e.gridUnit}px;
        display: flex;
        align-items: center;
        height: 100%;  &.antd5-menu-submenu-active {
    .antd5-menu-title-content {
      color: ${e.colors.primary.base};
    }
  }
  `}
`,{useBreakpoint:ie}=d.xA;function oe({data:{menu:e,brand:a,navbar_right:t,settings:n,environment_tag:i},isFrontendRoute:o=()=>!1}){const[f,y]=(0,r.useState)("horizontal"),_=ie(),x=(0,b.Q1)();let Y;(0,r.useEffect)((()=>{function e(){window.innerWidth<=767?y("inline"):y("horizontal")}e();const a=l()((()=>e()),10);return window.addEventListener("resize",a),()=>window.removeEventListener("resize",a)}),[]),function(e){e.Explore="/explore",e.Dashboard="/dashboard",e.Chart="/chart",e.Datasets="/tablemodelview"}(Y||(Y={}));const w=[],[C,S]=(0,r.useState)(w),A=(0,u.zy)();return(0,r.useEffect)((()=>{const e=A.pathname;switch(!0){case e.startsWith(Y.Dashboard):S(["Dashboards"]);break;case e.startsWith(Y.Chart)||e.startsWith(Y.Explore):S(["Charts"]);break;case e.startsWith(Y.Datasets):S(["Datasets"]);break;default:S(w)}}),[A.pathname]),(0,s.P3)(v.vX.standalone)||x.hideNav?(0,P.Y)(P.FK,{}):(0,P.Y)(ne,{className:"top",id:"main-menu",role:"navigation",children:(0,P.FD)(d.fI,{children:[(0,P.FD)(d.fv,{md:16,xs:24,children:[(0,P.Y)(h.m_,{id:"brand-tooltip",placement:"bottomLeft",title:a.tooltip,arrow:{pointAtCenter:!0},children:o(window.location.pathname)?(0,P.Y)(m.K,{className:"navbar-brand",to:a.path,children:(0,P.Y)("img",{src:a.icon,alt:a.alt})}):(0,P.Y)("a",{className:"navbar-brand",href:a.path,tabIndex:-1,children:(0,P.Y)("img",{src:a.icon,alt:a.alt})})}),a.text&&(0,P.Y)("div",{className:"navbar-brand-text",children:(0,P.Y)("span",{children:a.text})}),(0,P.Y)(c.NG,{mode:f,className:"main-nav",selectedKeys:C,disabledOverflow:!0,children:e.map(((e,a)=>{var t;return(({label:e,childs:a,url:t,index:n,isFrontendRoute:l})=>t&&l?(0,P.Y)(c.NG.Item,{role:"presentation",children:(0,P.Y)(p.k2,{role:"button",to:t,activeClassName:"is-active",children:e})},e):t?(0,P.Y)(c.NG.Item,{children:(0,P.Y)("a",{href:t,children:e})},e):(0,P.Y)(re,{title:e,icon:"inline"===f?(0,P.Y)(P.FK,{}):(0,P.Y)(g.F.CaretDownOutlined,{iconSize:"xs"}),children:null==a?void 0:a.map(((a,t)=>"string"==typeof a&&"-"===a&&"Data"!==e?(0,P.Y)(c.NG.Divider,{},`$${t}`):"string"!=typeof a?(0,P.Y)(c.NG.Item,{children:a.isFrontendRoute?(0,P.Y)(p.k2,{to:a.url||"",exact:!0,activeClassName:"is-active",children:a.label}):(0,P.Y)("a",{href:a.url,children:a.label})},`${a.label}`):null))},n))({index:a,...e,isFrontendRoute:o(e.url),childs:null==(t=e.childs)?void 0:t.map((e=>"string"==typeof e?e:{...e,isFrontendRoute:o(e.url)}))})}))})]}),(0,P.Y)(d.fv,{md:8,xs:24,children:(0,P.Y)(te,{align:_.md?"flex-end":"flex-start",settings:n,navbarRight:t,isFrontendRoute:o,environmentTag:i})})]})})}function se({data:e,...a}){const t={...e},n={Data:!0,Security:!0,Manage:!0},l=[],r=[];return t.menu.forEach((e=>{if(!e)return;const a=[],t={...e};e.childs&&(e.childs.forEach((e=>{("string"==typeof e||e.label)&&a.push(e)})),t.childs=a),n.hasOwnProperty(e.name)?r.push(t):l.push(t)})),t.menu=l,t.settings=r,(0,P.Y)(oe,{data:t,...a})}},85994:(e,a,t)=>{t.d(a,{A:()=>p});var n=t(96540),l=t(96453),r=t(67073),i=t(2445);const o=l.I4.label`
  cursor: pointer;
  display: inline-block;
  margin-bottom: 0;
`,s=(0,l.I4)(r.F.CheckboxHalf)`
  color: ${({theme:e})=>e.colors.primary.base};
  cursor: pointer;
`,d=(0,l.I4)(r.F.CheckboxOff)`
  color: ${({theme:e})=>e.colors.grayscale.base};
  cursor: pointer;
`,c=(0,l.I4)(r.F.CheckboxOn)`
  color: ${({theme:e})=>e.colors.primary.base};
  cursor: pointer;
`,h=l.I4.input`
  &[type='checkbox'] {
    cursor: pointer;
    opacity: 0;
    position: absolute;
    left: 3px;
    margin: 0;
    top: 4px;
  }
`,u=l.I4.div`
  cursor: pointer;
  display: inline-block;
  position: relative;
`,p=(0,n.forwardRef)((({indeterminate:e,id:a,checked:t,onChange:l,title:r="",labelText:p="",...m},g)=>{const b=(0,n.useRef)(),v=g||b;return(0,n.useEffect)((()=>{v.current.indeterminate=e}),[v,e]),(0,i.FD)(i.FK,{children:[(0,i.FD)(u,{children:[e&&(0,i.Y)(s,{}),!e&&t&&(0,i.Y)(c,{}),!e&&!t&&(0,i.Y)(d,{}),(0,i.Y)(h,{name:a,id:a,type:"checkbox",ref:v,checked:t,onChange:l,...m})]}),(0,i.Y)(o,{title:r,htmlFor:a,children:p})]})}))}}]);