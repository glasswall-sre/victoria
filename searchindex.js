Search.setIndex({docnames:["autoapi/index","autoapi/victoria/config/index","autoapi/victoria/encryption/azure_provider/index","autoapi/victoria/encryption/index","autoapi/victoria/encryption/provider/index","autoapi/victoria/encryption/schemas/index","autoapi/victoria/index","autoapi/victoria/plugin/index","autoapi/victoria/script/index","autoapi/victoria/script/victoria/index","autoapi/victoria/storage/azure_provider/index","autoapi/victoria/storage/index","autoapi/victoria/storage/local_provider/index","autoapi/victoria/storage/provider/index","autoapi/victoria/util/index","developer-guide","index","introduction","plugin-creation","user-guide"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":3,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":2,"sphinx.domains.rst":2,"sphinx.domains.std":1,sphinx:56},filenames:["autoapi/index.rst","autoapi/victoria/config/index.rst","autoapi/victoria/encryption/azure_provider/index.rst","autoapi/victoria/encryption/index.rst","autoapi/victoria/encryption/provider/index.rst","autoapi/victoria/encryption/schemas/index.rst","autoapi/victoria/index.rst","autoapi/victoria/plugin/index.rst","autoapi/victoria/script/index.rst","autoapi/victoria/script/victoria/index.rst","autoapi/victoria/storage/azure_provider/index.rst","autoapi/victoria/storage/index.rst","autoapi/victoria/storage/local_provider/index.rst","autoapi/victoria/storage/provider/index.rst","autoapi/victoria/util/index.rst","developer-guide.rst","index.rst","introduction.rst","plugin-creation.rst","user-guide.rst"],objects:{"":{victoria:[6,0,0,"-"]},"victoria.config":{APP_AUTHOR:[1,1,1,""],APP_NAME:[1,1,1,""],CONFIG_SCHEMA:[1,1,1,""],Config:[1,2,1,""],ConfigSchema:[1,2,1,""],DEFAULT_CONFIG_NAME:[1,1,1,""],EXAMPLE_CONFIG_FILE:[1,1,1,""],_handle_config_file_override:[1,5,1,""],_inject_core_config:[1,5,1,""],_print_validation_err:[1,5,1,""],ensure:[1,5,1,""],get_config_loc:[1,5,1,""],load:[1,5,1,""],load_plugin_config:[1,5,1,""],pass_config:[1,1,1,""]},"victoria.config.Config":{__eq__:[1,3,1,""],as_dict:[1,3,1,""],encryption_provider:[1,4,1,""],get_encryption:[1,3,1,""],get_storage:[1,3,1,""],logging_config:[1,4,1,""],plugins_config:[1,4,1,""],plugins_config_location:[1,4,1,""],storage_providers:[1,4,1,""]},"victoria.config.ConfigSchema":{encryption_provider:[1,4,1,""],logging_config:[1,4,1,""],make_config_obj:[1,3,1,""],plugins_config:[1,4,1,""],plugins_config_location:[1,4,1,""],storage_providers:[1,4,1,""]},"victoria.encryption":{EncryptionProvider:[3,1,1,""],EncryptionProviderConfig:[3,2,1,""],EncryptionProviderConfigSchema:[3,2,1,""],PROVIDERS_MAP:[3,1,1,""],azure_provider:[2,0,0,"-"],make_provider:[3,5,1,""],provider:[4,0,0,"-"],schemas:[5,0,0,"-"]},"victoria.encryption.EncryptionProviderConfig":{config:[3,4,1,""],provider:[3,4,1,""],to_yaml:[3,3,1,""]},"victoria.encryption.EncryptionProviderConfigSchema":{config:[3,4,1,""],make_encryption_provider_config:[3,3,1,""],provider:[3,4,1,""]},"victoria.encryption.azure_provider":{AzureEncryptionProvider:[2,2,1,""],CLIENT_ID_ENVVAR:[2,1,1,""],CLIENT_SECRET_ENVVAR:[2,1,1,""],ENCRYPTION_ALGORITHM:[2,1,1,""],TENANT_ID_ENVVAR:[2,1,1,""]},"victoria.encryption.azure_provider.AzureEncryptionProvider":{client_id:[2,4,1,""],client_secret:[2,4,1,""],crypto_client:[2,4,1,""],decrypt:[2,3,1,""],encrypt:[2,3,1,""],key_client:[2,4,1,""],rotate_key:[2,3,1,""],tenant_id:[2,4,1,""]},"victoria.encryption.provider":{EncryptionProvider:[4,2,1,""]},"victoria.encryption.provider.EncryptionProvider":{_data_decrypt:[4,3,1,""],_data_encrypt:[4,3,1,""],decrypt:[4,3,1,""],decrypt_str:[4,3,1,""],encrypt:[4,3,1,""],encrypt_str:[4,3,1,""],rotate_key:[4,3,1,""]},"victoria.encryption.schemas":{EncryptionEnvelope:[5,2,1,""],EncryptionEnvelopeSchema:[5,2,1,""],EncryptionProviderConfig:[5,2,1,""],EncryptionProviderConfigSchema:[5,2,1,""]},"victoria.encryption.schemas.EncryptionEnvelope":{data:[5,4,1,""],iv:[5,4,1,""],key:[5,4,1,""],version:[5,4,1,""]},"victoria.encryption.schemas.EncryptionEnvelopeSchema":{data:[5,4,1,""],iv:[5,4,1,""],key:[5,4,1,""],make_encryption_envelope:[5,3,1,""],version:[5,4,1,""]},"victoria.encryption.schemas.EncryptionProviderConfig":{config:[5,4,1,""],provider:[5,4,1,""],to_yaml:[5,3,1,""]},"victoria.encryption.schemas.EncryptionProviderConfigSchema":{config:[5,4,1,""],make_encryption_provider_config:[5,3,1,""],provider:[5,4,1,""]},"victoria.plugin":{Plugin:[7,2,1,""],load:[7,5,1,""],load_all:[7,5,1,""],ls:[7,5,1,""]},"victoria.plugin.Plugin":{__eq__:[7,3,1,""],cli:[7,4,1,""],config_schema:[7,4,1,""],name:[7,4,1,""]},"victoria.script":{victoria:[9,0,0,"-"]},"victoria.script.victoria":{CONTEXT_SETTINGS:[9,1,1,""],HELP_TEXT:[9,1,1,""],VERSION_NUMBER:[9,1,1,""],VictoriaCLI:[9,2,1,""],cli:[9,5,1,""],main:[9,5,1,""]},"victoria.script.victoria.VictoriaCLI":{get_command:[9,3,1,""],list_commands:[9,3,1,""]},"victoria.storage":{PROVIDERS_MAP:[11,1,1,""],StorageProvider:[11,1,1,""],azure_provider:[10,0,0,"-"],local_provider:[12,0,0,"-"],make_provider:[11,5,1,""],provider:[13,0,0,"-"]},"victoria.storage.azure_provider":{AzureStorageProvider:[10,2,1,""]},"victoria.storage.azure_provider.AzureStorageProvider":{client:[10,4,1,""],ls:[10,3,1,""],main_client:[10,4,1,""],retrieve:[10,3,1,""],store:[10,3,1,""]},"victoria.storage.local_provider":{LocalStorageProvider:[12,2,1,""]},"victoria.storage.local_provider.LocalStorageProvider":{_ensure_container:[12,3,1,""],container:[12,4,1,""],ls:[12,3,1,""],retrieve:[12,3,1,""],store:[12,3,1,""]},"victoria.storage.provider":{StorageProvider:[13,2,1,""]},"victoria.storage.provider.StorageProvider":{ls:[13,3,1,""],retrieve:[13,3,1,""],store:[13,3,1,""]},"victoria.util":{basenamenoext:[14,5,1,""]},victoria:{config:[1,0,0,"-"],encryption:[3,0,0,"-"],plugin:[7,0,0,"-"],script:[8,0,0,"-"],storage:[11,0,0,"-"],util:[14,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","data","Python data"],"2":["py","class","Python class"],"3":["py","method","Python method"],"4":["py","attribute","Python attribute"],"5":["py","function","Python function"]},objtypes:{"0":"py:module","1":"py:data","2":"py:class","3":"py:method","4":"py:attribute","5":"py:function"},terms:{"123":19,"2019":17,"2048":19,"256":[4,18],"38d":4,"800":4,"abstract":[4,13],"byte":[2,4,10,12,13,18],"case":[17,18],"class":[14,16,18,19],"default":[1,2,4,18,19],"final":[4,19],"function":[4,5,6,17,18],"import":[9,17,18],"long":19,"new":[2,4,16,19],"public":[4,19],"return":[1,2,3,4,7,11,18],"true":[18,19],"try":[16,18,19],AES:[4,18],And:[18,19],For:[4,7,17,18],Going:18,NOT:4,Not:17,The:[1,2,3,4,5,7,9,10,11,12,13,16,18,19],These:19,Used:[3,11],Uses:4,Using:19,With:17,__eq__:[1,7],__init__:[7,16],_data_decrypt:4,_data_encrypt:4,_ensure_contain:12,_handle_config_file_overrid:1,_inject_core_config:1,_print_validation_err:1,_str:18,a_plugin:19,a_subdir:19,abc:[4,13],abil:17,abl:[18,19],abov:[18,19],accept:[16,19],access:[16,19],account:[10,19],account_nam:[10,11,19],acknowledg:16,acronym:17,action:19,activ:[9,17],actual:19,add:19,adding:18,addition:19,address:16,advic:18,again:[18,19],all:[6,7,16,17,18,19],allow:[17,18,19],alreadi:19,also:[18,19],altern:19,analys:17,ani:[1,9,16,17,18,19],another_plugin:19,another_subdir:19,anymor:18,anyon:19,anyth:19,api:[7,10,16,18],api_kei:18,apipluginconfig:18,apipluginconfigschema:18,apowel:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,18],app:1,app_author:1,app_nam:1,appid:19,applic:[1,8,9],appreci:16,arbitrari:4,architectur:16,archiv:17,argument:[3,11,18,19],around:[17,18,19],as_dict:1,asap:4,ash:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,18],ask:19,assign:16,asymmetr:4,attempt:1,attr:9,august:17,auth:[2,10],auth_via_cli:[2,10,19],authent:[2,10,19],author:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,18],author_email:18,auto:0,autoapi:0,autom:[9,16],automat:16,avail:[9,18],azur:[2,3,10,11,16,18],azure_client_id:[2,19],azure_client_secret:[2,19],azure_provid:[0,3,6,11],azure_tenant_id:[2,19],azureencryptionprovid:2,azurestorageprovid:10,back:19,backend:16,backstori:16,base64:5,base:[1,2,3,4,5,9,10,12,13,18],basenam:14,basenamenoext:14,basic:[2,4],been:5,befor:[16,17],being:19,below:[16,19],bespok:17,best:[2,4,18],bit:[4,18],blob:[10,12,13,16,17,19],blobservicecli:10,block:19,board:16,bonjour:18,book:17,bool:[1,2,3,5,10],born:17,bot:17,both:19,bottom:19,branch:16,bread:9,brows:17,build:16,built:18,bunch:17,busi:16,butter:9,call:[1,3,9,11,16,18,19],can:[2,4,7,16,17,18,19],cannot:16,capac:17,certain:[17,18],cfg:[1,18],chang:[16,17,19],chat:17,check:[16,18],cipher:[4,18],circumst:4,classmethod:[3,5],cli:[2,7,8,9,10,16,17,18,19],click:[7,9,18],client:[2,10,19],client_id:[2,19],client_id_envvar:2,client_secret:[2,19],client_secret_envvar:2,clone:[15,16],cloud:[4,5,16,17,18],cls:[3,5],cmd_name:9,code:[16,19],codecov:16,com:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,18,19],combin:19,come:[17,19],command:[1,7,9,17,18,19],comment:17,commit:16,common:6,complex:[17,19],config:[0,3,5,6,7,16,17,19],config_fil:[9,19],config_for_a_plugin:19,config_path:1,config_schema:[1,7,18],configschema:1,configur:[16,17,18],congrat:16,conn:18,connect:[1,2,10,18,19],connection_str:[10,19],connectionstr:19,consequ:18,consol:19,constructor:[3,5,11],contain:[0,1,4,6,7,10,12,13,14,18,19],container_nam:19,containercli:10,content:16,context:[1,3,5],context_set:9,contributor:19,control:19,convent:16,core:[1,3,5,6,16,19],core_cfg:1,core_config:18,correct:17,correctli:[2,19],corrupt:17,could:[17,18,19],counter:[4,18],cov:16,coverag:16,creat:[0,1,7,16,18,19],create_config:18,create_hello_config:18,creation:[16,19],critic:19,crypto:2,crypto_cli:2,cryptographycli:2,csrc:4,ctiviti:16,ctx:9,current:19,custom:[7,17,18],customis:18,dai:16,data:[1,2,3,4,5,10,12,13,16,17,18,19],data_encryption_kei:4,date:[2,4,18,19],dead:17,decid:19,declar:18,decor:[1,18],decrypt:[2,4,18,19],decrypt_str:[4,18],decrypted_kei:18,def:18,default_config_nam:1,defin:[7,18,19],definit:18,dek:[18,19],del:18,delet:18,deploi:19,deploy:19,descript:[16,18],deseri:1,detail:[4,19],determinist:17,dev:15,develop:17,devop:18,dict:[1,3,5],didn:1,differ:[2,4,17,19],directli:19,directori:19,disabl:16,disable_existing_logg:19,do_api_th:18,doc:[4,5],docstr:16,document:0,doe:17,doesn:17,don:[2,4,18,19],done:19,download:17,dpath:19,dump_onli:[1,3,5],dumper:[3,5],dynam:17,each:[7,16],easi:[16,19],easili:18,edit:[18,19],educ:16,element:18,email:[16,17],enabl:19,encod:[4,5],encrupt:16,encrypt:[0,1,6,16,17,18],encrypt_str:[4,18],encryption_algorithm:2,encryption_provid:[1,19],encryptionenvelop:[2,4,5,18],encryptionenvelopeschema:[5,18],encryptionprovid:[1,2,3,4,18],encryptionproviderconfig:[1,3,5],encryptionproviderconfigschema:[3,5],end:16,enforc:16,ensur:[1,17,19],entri:[7,18],entrypoint:[7,8],envelop:[2,4,5,18,19],environ:[2,17,19],eri:16,err:1,error:[1,7,17],even:[17,19],event:18,eventu:17,ever:19,everi:[16,18],everyon:[17,19],everyth:16,exampl:[1,7,16,17,18],example_config_fil:1,except:18,exclud:[1,3,5],execut:[17,18],exist:1,exit:18,expect:16,exploit:16,exploratori:17,ext:19,extens:[14,16],extract:17,factori:[3,11],fail:[16,19],fairli:17,fals:[1,3,5,10],familiar:17,fanci:16,fast:17,featur:17,field:[3,5,18,19],figur:[16,17],file:[1,9,12,14,16,19],file_path:1,filenam:1,filepath:14,find:[17,19],find_packag:18,fix:16,folder:12,follow:[16,18,19],form:17,format:[7,16,18,19],formatt:19,found:[1,7,16,19],four:18,from:[1,3,7,9,10,11,12,13,16,17,19],further:[18,19],galoi:[4,18],gcm:4,gener:[0,4,10,12,13,16,17,19],get:[1,7,9,10,12,13,14,17,18,19],get_command:9,get_config_loc:1,get_encrypt:[1,18],get_storag:1,github:19,give:19,given:[1,2,3,4,10,11,12,13],glasswal:[17,19],glasswallsolut:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,18],glasswallsr:1,goe:[17,19],gone:17,good:[15,16],googl:[4,5,16,17,18],got:[16,19],gov:4,grab:[17,19],greet:18,group:[18,19],grow:17,had:[17,19],handl:[1,18,19],handler:19,has:[5,17,18,19],have:[1,16,17,18,19],hello:18,helloconfig:18,helloconfigschema:18,help:19,help_text:9,here:[16,18,19],high:17,highli:17,how:[17,18],http:[4,5,19],http_logging_polici:19,human:[1,17],iam:19,identifi:[1,17],impact:[16,17],imper:16,implement:[2,3,5,10,11,12],includ:[17,18],indent:19,inessenti:[9,17],info:[2,19],inform:[2,4,18],infrastructur:19,inhibit:[9,16],initi:18,inject:[1,18],inlin:19,insid:18,inspect:16,instal:[7,9,17,18],install_requir:18,instanc:[1,18],instead:19,integr:16,interact:19,interfac:17,intern:1,introduct:16,invalid:[1,3,11],iobas:[10,12,13],isol:19,issu:[16,19],its:[4,7,17],itself:18,json:19,just:[2,4,18,19],keep:19,kei:[1,2,4,5,10,12,13,16,18,19],kek:[2,4,16,18],key_client:2,key_nam:19,key_vault_url:19,keyclient:2,keyencryptionkei:19,keyvault:19,kind:19,kms:[4,5],know:[16,18],kty:19,kwarg:[1,2,3,5,11,12,18],latest:[2,4],least:16,leav:19,length:4,let:[18,19],letter:17,level:19,liabl:18,like:[1,16,18,19],line:17,link:16,lint:16,list:[7,9,10,12,13,19],list_command:9,load:[1,6,7,9,17,19],load_al:7,load_onli:[1,3,5],load_plugin_config:1,loaded_config:1,local:[12,16,19],local_provid:[0,6,11],localstorageprovid:12,locat:[1,7,19],log:[1,18,19],logger:19,logging_config:[1,18,19],login:19,longer:18,look:17,lot:[17,19],machin:19,made:19,mai:[16,17,19],main:[1,8,9,19],main_client:10,mainli:17,make:[1,3,11,16,17,18,19],make_config_obj:1,make_encryption_envelop:5,make_encryption_provider_config:[3,5],make_provid:[3,11],manag:19,mani:[1,3,5,16,17],manipul:18,manual:17,map:[1,3,5,11,19],marshal:1,marshmallow:[1,3,5,7,18],mass:17,master:16,mean:19,member:17,memori:18,merg:16,messag:[16,19],method:[1,4,18],microservic:17,might:18,mind:18,minim:[17,18],minimis:16,mit:16,mode:[4,18],modifi:18,modul:[18,19],mond:18,mood:16,more:[4,17,18,19],mportant:16,much:17,multicommand:9,multipl:[9,16],must:[7,18],name:[1,2,3,7,9,10,11,12,13,16,17,18,19],narg:18,necessari:[16,19],need:[16,17,18,19],nessenti:16,nest:18,net:19,newli:[2,4],nist:[4,18],nonc:[4,5,18,19],none:[1,2,3,4,5,7,9,10,12,13,18],normal:[3,11,19],note:[2,4,18,19],now:[17,18,19],number:[9,16,17],object:[1,4,7,18,19],objectid:19,obvious:[18,19],occasion:19,occur:1,off:[16,19],oil:16,old:[2,4,18,19],ommand:16,onc:17,one:[16,18,19],onli:[1,3,5,10,16,17,19],opportun:18,optim:9,optimis:17,option:[2,4,7],order:[18,19],other:[1,7,16,19],otherwis:[18,19],our:[16,17,18],out:[2,4,16,17,18,19],outdat:18,output:[16,19],over:19,overrid:[1,9],override_loc:1,overwitten:18,own:17,packag:[7,16,17],page:0,param:[3,5],paramet:[1,2,3,4,7,10,11,12,13,18],part:16,partial:[1,3,5],pass:[1,3,5,18],pass_config:1,pass_obj:18,password:19,past:[18,19],path:[1,10,12,13,14,19],pbi:[18,19],peopl:[16,19],perform:19,perform_some_api_act:18,perhap:[17,18],permiss:19,pick:16,piec:[4,10,12,13,16,19],piggyback:19,pip:[16,19],pipelin:19,pipenv:15,place:17,plaintext:[4,18,19],plan:17,platform:17,pleas:[2,4,16,18,19],pluggabl:[9,16],plugin:[0,1,6,9,16,17],plugin_nam:[7,18],plugins_config:[1,7,18,19],plugins_config_loc:[1,19],poetri:16,point:[7,18,19],polici:19,post_load:18,powel:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,18],power:17,pprint:18,practic:18,preced:19,prefer:16,prefix:7,preinstal:19,previou:18,previous:19,princip:[2,19],print:[1,9,18,19],privat:[16,18],probabl:[2,4],problem:[16,17],process:[17,18],product:[9,16],project:19,properti:18,protect:19,provid:[0,1,2,3,5,6,10,11,12,16,18,19],provider_typ:[3,11],providers_map:[3,11],ptimiz:16,publicli:16,pulumi:19,put:[17,18,19],pylint:16,pytest:16,python:[7,9,15,16,17,18,19],queri:19,quick:19,quickli:17,quit:19,rais:[1,2,3,11,18],rbac:19,readabl:1,readi:[16,18],readm:19,rebuild:17,recommend:[4,16,18],redeploi:17,reduc:[9,17],reencrypt:[2,4],refactor:16,refer:16,reliabl:17,rememb:19,remot:[17,19],remov:19,replac:19,replai:17,repo:[15,16,18],requir:[17,18,19],reserv:18,resourc:19,respect:19,respons:17,rest:[16,18,19],result:18,retriev:[10,12,13],reus:4,review:16,rework:16,rid:18,rife:17,right:19,risk:17,root:19,rotat:[2,4,16,18],rotate_kei:[2,4],rsa:19,run:[15,16,17,18,19],runtim:7,saa:17,safe:18,sai:[17,19],same:[1,4,7,18,19],save:16,schema:[0,1,3,6,7,18],script:[0,6,16,17],secret:[2,16,17,19],section:[1,18,19],secur:[16,18,19],see:[3,4,5,11,18,19],self:[1,2,3,4,5,7,9,10,12,13,18],send:16,sensit:[17,18,19],separ:[18,19],sequenc:4,serverless:17,servic:[2,10,18,19],set:[18,19],setup:16,setuptool:18,share:[17,19],should:[2,7,10,18,19],show:19,sign:16,simpl:19,simpli:18,singl:[9,16],situat:17,size:19,sku:19,small:16,softwar:19,solut:[17,19],solv:17,some:[1,7,17,18],some_api:18,some_config:19,some_other_modul:18,some_plugin:[18,19],some_valu:19,someon:[16,18],someth:17,sometim:17,somewher:[17,19],sonarcloud:16,soon:18,sourc:[1,19],sp_object_id:19,space:17,specif:[2,3,4,11,17],specifi:[2,4,16,19],sphinx:0,sre:[9,16,17,19],stack:19,stand:17,standard:19,start:[7,17,18],statu:18,stdout:[18,19],steal:18,stock:16,storag:[0,1,6,16,17,18],storage_account_nam:19,storage_provid:[1,19],storageprovid:[1,10,11,12,13],storagev2:19,store:[1,3,4,5,10,12,13,16,17,19],str:[1,2,3,4,5,7,10,11,12,13,14,18],stream:[10,12,13,19],streamhandl:19,string:[4,10,19],strsequenceorset:[1,3,5],structur:16,stuff:19,stvictoria:19,style:16,sub:[18,19],subcommand:[7,9,16,18,19],subject:16,submit:16,submodul:16,subpackag:16,successfulli:7,suggest:16,suitabl:19,super_secret_access_kei:19,support:[9,17,19],sure:[1,16,17,18,19],sync:[15,17],sys:19,system:[7,9,17,19],systemexit:18,tag_nam:18,take:[17,19],task:[9,16,17],team:[17,19],templat:[16,19],tenant:[2,19],tenant_id:[2,19],tenant_id_envvar:2,tend:17,test:[16,19],text:19,the_config_for_some_plugin:19,thei:[16,18,19],them:[16,17,18,19],thi:[0,1,2,4,6,7,8,9,16,17,18,19],thing:17,three:18,through:19,time:17,to_yaml:[3,5],toil:[9,16,17],too:[16,17],tool:17,toolbelt:[9,16],top:19,transmit:18,transpar:17,tsv:19,tupl:4,two:19,type:[1,2,3,4,5,7,10,11,12,18],typeerror:[2,3,11],uksouth:19,unassign:16,under:[4,7,16,18],union:[1,2,3,4,5,10,12,13],unknown:[1,3,5],unwieldi:17,updat:[17,19],url:[2,19],usag:[17,19],use:[1,2,4,7,10,16,17,18,19],used:[1,4,5,7,10,14,18,19],useful:[17,19],user:[16,17,18],uses:[9,18,19],using:[12,16,18,19],usual:18,utf:4,util:[0,6,16],valid:[1,7],validationerror:1,valu:[1,4,7,17,18,19],valueerror:[1,3,11],variabl:[2,19],variou:[1,14,17],vault:[2,16,19],vault_url:[2,3,19],vector:18,verb:19,veri:[9,17],version:[2,4,5,9,17,18,19],version_numb:9,via:[2,10,17,19],victoria:[0,16,19],victoria_:[7,18],victoria_cloud_backend:19,victoria_config:[7,18],victoria_exampl:1,victoria_pbi:18,victoria_storag:19,victoriacli:9,victoriaserviceprincip:19,vscode:19,wai:[17,19],want:[2,4,18,19],wasn:1,watch:[17,19],well:[17,18,19],went:17,were:[3,11,17,19],what:[1,17,18],whatev:[1,18,19],when:[4,9,16,17,18,19],whenev:16,where:19,wherev:19,whether:10,which:19,whilst:7,who:1,why:16,wire:7,wish:17,within:[10,12,13,16,18,19],without:[7,14,16],won:18,work:[16,17,18,19],world:18,would:[3,11,16,18,19],wouldn:18,wrap:17,write:17,written:17,wrong:[3,11,17,19],wrote:17,xxx:19,yaml:[1,18,19],yapf:16,yield:[10,12,13],you:[2,3,4,11,15,16,17,18,19],young:17,your:[4,16,17,18,19],yourself:16,youself:17},titles:["API Reference","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">victoria.config</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">victoria.encryption.azure_provider</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">victoria.encryption</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">victoria.encryption.provider</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">victoria.encryption.schemas</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">victoria</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">victoria.plugin</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">victoria.script</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">victoria.script.victoria</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">victoria.storage.azure_provider</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">victoria.storage</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">victoria.storage.local_provider</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">victoria.storage.provider</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">victoria.util</span></code>","Developer Guide","V.I.C.T.O.R.I.A.","Introduction","Plugin Creation","User Guide"],titleterms:{"class":[1,2,3,4,5,7,9,10,12,13],"function":[1,3,7,9,11,14],__init__:18,access:18,api:0,azur:19,azure_provid:[2,10],backend:19,backstori:17,bug:16,call:17,cloud:19,config:[1,18],configur:19,content:[1,2,3,4,5,7,9,10,11,12,13,14],contribut:16,core:18,creation:18,develop:[15,16],document:16,encrypt:[2,3,4,5,19],exampl:19,featur:16,file:18,from:18,gener:18,guid:[15,16,19],instal:[16,19],introduct:17,kek:19,licens:16,local_provid:12,modul:[1,2,4,5,7,9,10,12,13,14],packag:[3,11,18],plugin:[7,18,19],prerequisit:[15,16,19],provid:[4,13],pull:16,quick:[15,16],refer:0,report:16,request:16,rotat:19,schema:5,script:[8,9],secret:18,setup:18,specifi:18,start:[15,16],stock:19,storag:[10,11,12,13,19],store:18,structur:18,submodul:[3,6,8,11],subpackag:6,user:19,util:14,victoria:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,17,18],vulner:16,why:17}})