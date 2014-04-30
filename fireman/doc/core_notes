This text contains preliminary notes regarding the core implementation and interface. Other considerations that are somehow related will be written here too.

These are preliminary, and as such will not necessarily be kept up to date.

Where examples are helpful, they might be given under the assumption that iptables underlies the core, but this may not be so.

The core must provide the following:
  It will present an API sufficient for at least both a CLI and for a service listener.
  It will present configuration files for itself, and configuration files to configure the firewall rules.
  It will provide some functionality to automatically generate firewall rule configurations to some extent.
  It will pass these rules to a rule translation engine.

The BARE minimum the rule translation engine must support for the core to operate is:
  Functionality for adding a rule with an identifying string to the underlying firewall software.
  Functionaliy for deleting a rule based on an identifying string.
  A common representation for a rule.

The core will not be a daemon. It will be an API that is run by any process that requires its services.

Functions the API should provide:
1---
  Function for adding a service with an arbitrary string as a name
  Function for deleting a service by its name
  Function for adding some sort of filter rules to a service
  Function for deleting rules from a service
  Function for printing rules - by service or ALL
2---
  Function for getting all service names
  Function to lock the core so that no other process can run it without error
  Function to release the lock on the core
  Function to force the core - run it disregarding locks
  Function to return a file handle that can be read from whenever there are changes to available services
  Function for stopping a service
  Function for starting a service
3---
  Function for synchronising internal rules with underlying firewall implementation. Here "internal rules" refers to the rules defined in the config files.
  Function for automatically generating config files in some way. Perhaps there will be a config file for each service available, and generation can be discriminated by service name.

Justification:
1---
  The first 4 functions are standard functionalities that the CLI should provide
2---
  The next 5 functions imply a protocol to allow the service listener to operate, this is a little bit complicated by the fact that the core is an API not a daemon. The protocol is as follows:
    The service listener would lock the core
    The service listener would get a file handle that signals an event
    The service listener would read the list of available service names
    The service listener would unlock the core
    The locking prevents race conditions. The file handle received here would be used in some sort of event loop to watch for changes to the available services, so that the service listener can respond appropriately (by adjusting what it listens to)
    If the service listener ever deems it necessary, it would call the stop or start service functions
3---
  These allow config files to be generated, and to meaningful once changed.
 
Some ideas on semantics of rules/services. These are proposed ideas that MUST be discussed with the team, they have significant influence on the direction of our project. These ideas are described in terms of iptables, but should be extented to whatever the underlying firewall is:

---What?---
  When a service is added, it must be associated with a port (more generally: a protocol endpoint for protocols that don't have ports like ICMP). This will add a rule to the start of the default chain whenever the service is activated. This rule will match packets based only on whether its port matches the service's. It will then pass the packet to a service specific chain.

  When rules are added for a service, they are added only to the service specific chain.

---Why?---
  This makes services atomic, which makes the interface MUCH simpler. Now nobody has to worry about the order that services appear in (unless the rte/core wants to perform optimisations).

  Per service rules are not atomic so their order matters.

  Service specific rules now don't have to be concerned with rules for other services. Each service's chain will only get packets for its port, and it is guaranteed packets for its port.

  The core interface is much simpler because now we don't have to even address the ordering of services.

  This makes the firewall potentially slower, but much easier to configure and less troublesome. Firewall rule writing logic becomes much simpler.

--Concerns---
  On the one hand, the model is slower. The atomicity of services however allows for easy optimisation: reorder services based on their traffic, and behaviour won't be affected.

  This model is more rigid. To help remedy this I would suggest two "special" services: "init" and "final". These would not be bound to any ports, and these services can never be removed. init's rules are guaranteed to appear before any normal services rules, and final's rules are guaranteed to appear after any normal service rules. This allows for the idea of "global" rules. For example, we could add a filter rule in init to drop packets that aren't part of the local network, which would result in only packets from the local network arriving at services, regardless of the service rules.
  
  Given the init and final services, the rigidity is removed. It is still possible to use our tool as if services didn't behave as described using init and final. But, adding service specific rules has the advantages of: simplicity, possiblity of rule reordering and dynamic rule removal/adding.
