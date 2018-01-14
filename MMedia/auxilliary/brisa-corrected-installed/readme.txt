Folder brisa was copied from /usr/local/lib/python2.7/dist-packages/
The following files had tabs instead of spaces for indentation and these tabs messed up the entire file. Compare with the originally installed files which are in /media/Elements-ext3/manual_backup/brisa-original-installed-code.tar.gz


Find them in the untarred-unzipped archive with
grep -PRn "\t" * | grep -v "\.pyc:" | grep -v "^Binary" | grep -v "\.xml:"

brisa/core/network_listeners.py:97:	self.observers = [] if observers == None else observers
brisa/upnp/control_point/action.py:36:	self.service._soap_service.soap_header = self.service.call_headers
brisa/upnp/control_point/action.py:37:	if "call_headers" in kwargs:
brisa/upnp/control_point/action.py:38:	    self.service._soap_service.soap_header = kwargs.pop("call_headers",
brisa/upnp/control_point/action.py:39:	                                                        {})
brisa/upnp/control_point/action.py:41:	self.service._soap_service.soap_header = self.service.call_headers
brisa/upnp/control_point/action.py:42:	return response
brisa/upnp/control_point/control_point.py:137:    		     http_version="1.1", man='"ssdp:discover"', mx=1,
brisa/upnp/control_point/control_point.py:138:		     additionals={}):
brisa/upnp/control_point/control_point.py:148:			    in the end of the m-search message (default is
brisa/upnp/control_point/control_point.py:149:			    a empty dictionary)
brisa/upnp/control_point/control_point.py:163:			    additionals)
brisa/upnp/control_point/control_point.py:171:    			man='"ssdp:discover', mx=1, additionals={}):
brisa/upnp/control_point/control_point.py:176:	additionals parameter is used to add additional fields in the
brisa/upnp/control_point/control_point.py:177:	M-SEARCH message.
brisa/upnp/control_point/control_point.py:184:			    in the end of the m-search message (default is
brisa/upnp/control_point/control_point.py:185:			    a empty dictionary)
brisa/upnp/control_point/control_point.py:194:				      additionals)
brisa/upnp/control_point/control_point.py:257:	device.additional_headers = device_info['ADDITIONAL_HEADERS']
brisa/upnp/control_point/service.py:82:	@param call_headers: in case it is necessary to pass fields in the soap
brisa/upnp/control_point/service.py:83:	                     headers of each call.
brisa/upnp/control_point/msearch.py:71:	      man='"ssdp:discover"', mx=1, additionals={}):
brisa/upnp/control_point/msearch.py:80:			    in the end of the m-search message (default is
brisa/upnp/control_point/msearch.py:81:			    a empty dictionary)
brisa/upnp/control_point/msearch.py:91:	    self.ssdp.search_type = search_type
brisa/upnp/control_point/msearch.py:94:	    			   additionals, )
brisa/upnp/control_point/msearch.py:120:    			http_version="1.1", man='"ssdp:discover"', mx=1,
brisa/upnp/control_point/msearch.py:121:			additionals={}):
brisa/upnp/control_point/msearch.py:126:		 MX=%d, additionals=%s" % (search_type, http_version, man, mx,
brisa/upnp/control_point/msearch.py:127:		 			   additionals))
brisa/upnp/control_point/msearch.py:131:    		 man='"ssdp:discover"', mx=1, additionals={}):
brisa/upnp/control_point/msearch.py:137:	if (mx > 120):
brisa/upnp/control_point/msearch.py:138:	    mx = 120
brisa/upnp/control_point/msearch.py:139:	elif (mx < 1):
brisa/upnp/control_point/msearch.py:140:	    mx = 1
brisa/upnp/control_point/msearch.py:146:	append = req.append
brisa/upnp/control_point/msearch.py:147:	[append('%s: %s' % (k, v)) for k, v in additionals.items()]
brisa/upnp/control_point/msearch.py:148:	append('')
brisa/upnp/control_point/msearch.py:149:	append('')
brisa/upnp/base_device.py:133:	    service.device = self
brisa/upnp/soap.py:110:	    for header_name, header_args_dict in header_args.iteritems():
brisa/upnp/soap.py:111:	        header_name_elem = ElementTree.SubElement(header, header_name)
brisa/upnp/soap.py:112:		if isinstance(header_args_dict, dict):
brisa/upnp/soap.py:121:			                                        header_arg_type)
brisa/upnp/soap.py:125:	    log.error("Ignoring soap header due to malformed header_args dict")
brisa/upnp/soap.py:126:	    print str(e)
brisa/upnp/soap.py:204:    	for e in list(header):
brisa/upnp/soap.py:205:	    kwargs['__header__'][e.tag] = {}
brisa/upnp/soap.py:206:	    for se in list(e):
brisa/upnp/soap.py:207:	        kwargs['__header__'][e.tag][se.tag] = {}
brisa/upnp/soap.py:208:	        kwargs['__header__'][e.tag][se.tag]['__value__'] = __decode_result(se)
brisa/upnp/soap.py:209:	        kwargs['__header__'][e.tag][se.tag]['__attrib__'] = se.attrib
brisa/upnp/soap.py:242:	if isinstance(soap_header, dict):
brisa/upnp/soap.py:244:	                               for k, v in soap_header.iteritems())
brisa/upnp/soap.py:245:	else:
brisa/upnp/soap.py:246:	    self.soap_header = {}
brisa/upnp/soap.py:265:				  header_args=self.soap_header)
brisa/upnp/soap.py:266:	try:
brisa/upnp/soap.py:267:	    result = HTTPTransport().call(self.url, payload, ns,
brisa/upnp/base_service_builder.py:55:	    raise Exception(str(e)) 
brisa/upnp/base_service_builder.py:106:	    append = args.append
brisa/upnp/base_service_builder.py:108:	    	if arg_state_var is not None:
brisa/upnp/base_service_builder.py:109:		    arg_state_var = self.service._state_variables[arg_state_var]
brisa/upnp/base_service_builder.py:110:		append(self._create_argument(arg_name, arg_direction, arg_state_var))
brisa/upnp/ssdp.py:45:		search_type="sspd:all", additional_headers={}):
brisa/upnp/ssdp.py:63:	self.http_version = http_version
brisa/upnp/ssdp.py:67:	self.additional_headers = additional_headers
brisa/upnp/ssdp.py:68:	self.search_type = search_type
brisa/upnp/ssdp.py:203:	# TODO: check http version
brisa/upnp/ssdp.py:205:	   and headers['man'] == '"ssdp:discover"':
brisa/upnp/ssdp.py:210:	    if not self.receive_notify:
brisa/upnp/ssdp.py:212:              	log.debug('Received NOTIFY command from %s:%s (ignored '\
brisa/upnp/ssdp.py:215:              	return
brisa/upnp/ssdp.py:216:	    if self.search_type != "upnp:rootdevice" and \
brisa/upnp/ssdp.py:217:	        self.search_type != "sspd:all" and \
brisa/upnp/ssdp.py:218:	        self.search_type != headers['nt']:
brisa/upnp/ssdp.py:220:              	log.debug('Received NOTIFY command from %s:%s (ignored '\
brisa/upnp/ssdp.py:222:			'than headers["nt"])',
brisa/upnp/ssdp.py:224:              	return
brisa/upnp/ssdp.py:242:	for dev_info in self.known_device.values():
brisa/upnp/ssdp.py:243:	    if (headers['st'] == 'ssdp:all' or dev_info['ST'] == headers['st']):
brisa/upnp/ssdp.py:244:        	response = []
brisa/upnp/ssdp.py:245:	        append = response.append
brisa/upnp/ssdp.py:246:	        append('HTTP/%s 200 OK' % self.http_version)
brisa/upnp/ssdp.py:247:		additional_headers = dev_info.pop("ADDITIONAL_HEADERS", {})
brisa/upnp/ssdp.py:248:	        [append('%s: %s' % (k, v)) for k, v in dev_info.items()]
brisa/upnp/ssdp.py:249:		[append('%s: %s' % (k, v)) for k, v in additional_headers.items()]
brisa/upnp/ssdp.py:250:		dev_info['ADDITIONAL_HEADERS'] = additional_headers
brisa/upnp/ssdp.py:251:	        response.extend(('', ''))
brisa/upnp/ssdp.py:252:	        delay = random.randint(0, int(headers['mx']))
brisa/upnp/ssdp.py:253:	        # Avoid using a timer with delay 0 :)
brisa/upnp/ssdp.py:254:	        if delay:
brisa/upnp/ssdp.py:255:	            self.udp_transport.send_delayed(delay, '\r\n'.join(response),
brisa/upnp/ssdp.py:256:	                                            host, port)
brisa/upnp/ssdp.py:257:	        else:
brisa/upnp/ssdp.py:258:	            self.udp_transport.send_data('\r\n'.join(response),
brisa/upnp/ssdp.py:259:		    				    host, port)
brisa/upnp/ssdp.py:260:	        log.debug('Discovery request response sent to (%s, %d)',
brisa/upnp/ssdp.py:261:						    host, port)
brisa/upnp/ssdp.py:329:		                      'ADDITIONAL_HEADERS': additional_headers}
brisa/upnp/ssdp.py:337:		                      'ADDITIONAL_HEADERS': ""}
brisa/upnp/ssdp.py:410:		'HOST: %s:%d' % (SSDP_ADDR, SSDP_PORT),
brisa/upnp/ssdp.py:417:	append = response.append
brisa/upnp/ssdp.py:418:	[append('%s: %s' % (k, v)) for k, v in self.additional_headers.items()]
brisa/upnp/ssdp.py:420:	log.debug('Sending notify message with content %s' % response)
brisa/upnp/ssdp.py:421:	try:
brisa/upnp/ssdp.py:422:	    self.udp_transport.send_data('\r\n'.join(response), SSDP_ADDR, SSDP_PORT)
brisa/upnp/ssdp.py:424:	except Exception, e:
brisa/upnp/ssdp.py:425:	    log.info("Failure sending notify with message %s" % str(e))
brisa/upnp/base_service.py:51:	@type call_headers: dict
brisa/upnp/base_service.py:80:	self.call_headers = call_headers
brisa/upnp/base_service.py:81:	self.device = None 	# device using this service
brisa/upnp/base_service.py:107:    		 data_type=None, values=None):
brisa/upnp/device/action.py:73:	    if arg_name != '__header__':
brisa/upnp/device/action.py:82:	        if arg.state_var:
brisa/upnp/device/action.py:83:	            arg.state_var.update(arg_value)
brisa/upnp/device/action.py:90:	    msg = 'returned value from service function is not a dict.'
brisa/upnp/device/action.py:99:	    if arg_name != '__header__':
brisa/upnp/device/action.py:109:	        if arg.state_var:
brisa/upnp/device/action.py:110:            	    arg.state_var.update(arg_value)
brisa/upnp/device/action.py:114:	if "__header__" in out_kwargs:
brisa/upnp/device/action.py:117:	            "__header__": header}
brisa/upnp/device/device.py:57:	@param additional_ssdp_headers: can be used to add more field in the
brisa/upnp/device/device.py:83:			       additional_headers=additional_ssdp_headers)
brisa/upnp/device/xml_gen.py:226:	    if arg.state_var is not None:
brisa/upnp/device/xml_gen.py:227:	        element = SubElement(arg_element, "relatedStateVariable")
brisa/upnp/device/xml_gen.py:228:        	element.text = arg.state_var.name
brisa/upnp/device/service.py:85:	try:
brisa/upnp/device/service.py:86:	        data = request.read()
brisa/upnp/device/service.py:87:	except RuntimeError, e:
brisa/upnp/device/service.py:88:		return [str(e)]
brisa/upnp/device/service.py:122:	try:
brisa/upnp/device/service.py:124:	    force_use_header = False
brisa/upnp/device/service.py:125:	    if "__header__" in result:
brisa/upnp/device/service.py:127:		force_use_header = True
brisa/upnp/device/service.py:128:	except Exception, e:
brisa/upnp/device/service.py:129:	    # TODO: Create a soap exception to return to the remote requester
brisa/upnp/device/service.py:130:	    log.debug(str(e))
brisa/upnp/device/service.py:131:	    print str(e)
brisa/upnp/device/service.py:141:	if not force_use_header:
brisa/upnp/device/service.py:142:	    header_args = self.service.call_headers
brisa/upnp/device/service.py:146:					header_args=header_args)
brisa/upnp/device/service.py:194:		 spec_restricted=False):
brisa/upnp/device/service.py:202:	self.spec_restricted = spec_restricted
brisa/upnp/device/service.py:206:    							'event_reload_time'))
brisa/upnp/device/service.py:229:	    	ServiceBuilder(self, fd).build()
brisa/upnp/device/service.py:230:	    except Exception, e:
brisa/upnp/device/service.py:232:					'%s' % (id, str(e)))
brisa/upnp/device/service.py:239:	if (self.spec_restricted) and not len(self.get_variables()):




or just the files with 
grep -PRl "\t" * | grep -v "\.pyc" | grep -v "^Binary" | grep -v "\.xml"

brisa/core/network_listeners.py
brisa/upnp/control_point/action.py
brisa/upnp/control_point/control_point.py
brisa/upnp/control_point/service.py
brisa/upnp/control_point/msearch.py
brisa/upnp/base_device.py
brisa/upnp/soap.py
brisa/upnp/base_service_builder.py
brisa/upnp/ssdp.py
brisa/upnp/base_service.py
brisa/upnp/device/action.py
brisa/upnp/device/device.py
brisa/upnp/device/xml_gen.py
brisa/upnp/device/service.py
