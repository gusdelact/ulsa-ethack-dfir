# NIST CSF 2.0 Core (copia exportada)

Generado con `build_core.py` desde la exportación oficial del CPRT de NIST (`csf-2.0-core-cprt.json`). Textos en inglés, tal como los publica NIST. Fuente: <https://csrc.nist.gov/projects/cprt>

Funciones: 6 · Categorías: 22 · Subcategorías vigentes: 106

## GV GOVERN

The organization's cybersecurity risk management strategy, expectations, and policy are established, communicated, and monitored

### GV.OC Organizational Context

The circumstances - mission, stakeholder expectations, dependencies, and legal, regulatory, and contractual requirements - surrounding the organization's cybersecurity risk management decisions are understood

- **GV.OC-01**: The organizational mission is understood and informs cybersecurity risk management
  - Ejemplo: Share the organization's mission (e.g., through vision and mission statements, marketing, and service strategies) to provide a basis for identifying risks that may impede that mission
- **GV.OC-02**: Internal and external stakeholders are understood, and their needs and expectations regarding cybersecurity risk management are understood and considered
  - Ejemplo: Identify relevant internal stakeholders and their cybersecurity-related expectations (e.g., performance and risk expectations of officers, directors, and advisors; cultural expectations of employees)
  - Ejemplo: Identify relevant external stakeholders and their cybersecurity-related expectations (e.g., privacy expectations of customers, business expectations of partnerships, compliance expectations of regulators, ethics expectations of society)
- **GV.OC-03**: Legal, regulatory, and contractual requirements regarding cybersecurity - including privacy and civil liberties obligations - are understood and managed
  - Ejemplo: Determine a process to track and manage legal and regulatory requirements regarding protection of individuals' information (e.g., Health Insurance Portability and Accountability Act, California Consumer Privacy Act, General Data Protection Regulation)
  - Ejemplo: Determine a process to track and manage contractual requirements for cybersecurity management of supplier, customer, and partner information
  - Ejemplo: Align the organization's cybersecurity strategy with legal, regulatory, and contractual requirements
- **GV.OC-04**: Critical objectives, capabilities, and services that external stakeholders depend on or expect from the organization are understood and communicated
  - Ejemplo: Establish criteria for determining the criticality of capabilities and services as viewed by internal and external stakeholders
  - Ejemplo: Determine (e.g., from a business impact analysis) assets and business operations that are vital to achieving mission objectives and the potential impact of a loss (or partial loss) of such operations
  - Ejemplo: Establish and communicate resilience objectives (e.g., recovery time objectives) for delivering critical capabilities and services in various operating states (e.g., under attack, during recovery, normal operation)
- **GV.OC-05**: Outcomes, capabilities, and services that the organization depends on are understood and communicated
  - Ejemplo: Create an inventory of the organization's dependencies on external resources (e.g., facilities, cloud-based hosting providers) and their relationships to organizational assets and business functions
  - Ejemplo: Identify and document external dependencies that are potential points of failure for the organization's critical capabilities and services, and share that information with appropriate personnel

### GV.RM Risk Management Strategy

The organization's priorities, constraints, risk tolerance and appetite statements, and assumptions are established, communicated, and used to support operational risk decisions

- **GV.RM-01**: Risk management objectives are established and agreed to by organizational stakeholders
  - Ejemplo: Update near-term and long-term cybersecurity risk management objectives as part of annual strategic planning and when major changes occur
  - Ejemplo: Establish measurable objectives for cybersecurity risk management (e.g., manage the quality of user training, ensure adequate risk protection for industrial control systems)
  - Ejemplo: Senior leaders agree about cybersecurity objectives and use them for measuring and managing risk and performance
- **GV.RM-02**: Risk appetite and risk tolerance statements are established, communicated, and maintained
  - Ejemplo: Determine and communicate risk appetite statements that convey expectations about the appropriate level of risk for the organization
  - Ejemplo: Translate risk appetite statements into specific, measurable, and broadly understandable risk tolerance statements
  - Ejemplo: Refine organizational objectives and risk appetite periodically based on known risk exposure and residual risk
- **GV.RM-03**: Cybersecurity risk management activities and outcomes are included in enterprise risk management processes
  - Ejemplo: Aggregate and manage cybersecurity risks alongside other enterprise risks (e.g., compliance, financial, operational, regulatory, reputational, safety)
  - Ejemplo: Include cybersecurity risk managers in enterprise risk management planning
  - Ejemplo: Establish criteria for escalating cybersecurity risks within enterprise risk management
- **GV.RM-04**: Strategic direction that describes appropriate risk response options is established and communicated
  - Ejemplo: Specify criteria for accepting and avoiding cybersecurity risk for various classifications of data
  - Ejemplo: Determine whether to purchase cybersecurity insurance
  - Ejemplo: Document conditions under which shared responsibility models are acceptable (e.g., outsourcing certain cybersecurity functions, having a third party perform financial transactions on behalf of the organization, using public cloud-based services)
- **GV.RM-05**: Lines of communication across the organization are established for cybersecurity risks, including risks from suppliers and other third parties
  - Ejemplo: Determine how to update senior executives, directors, and management on the organization's cybersecurity posture at agreed-upon intervals
  - Ejemplo: Identify how all departments across the organization - such as management, operations, internal auditors, legal, acquisition, physical security, and HR - will communicate with each other about cybersecurity risks
- **GV.RM-06**: A standardized method for calculating, documenting, categorizing, and prioritizing cybersecurity risks is established and communicated
  - Ejemplo: Establish criteria for using a quantitative approach to cybersecurity risk analysis, and specify probability and exposure formulas
  - Ejemplo: Create and use templates (e.g., a risk register) to document cybersecurity risk information (e.g., risk description, exposure, treatment, and ownership)
  - Ejemplo: Establish criteria for risk prioritization at the appropriate levels within the enterprise
  - Ejemplo: Use a consistent list of risk categories to support integrating, aggregating, and comparing cybersecurity risks
- **GV.RM-07**: Strategic opportunities (i.e., positive risks) are characterized and are included in organizational cybersecurity risk discussions
  - Ejemplo: Define and communicate guidance and methods for identifying opportunities and including them in risk discussions (e.g., strengths, weaknesses, opportunities, and threats [SWOT] analysis)
  - Ejemplo: Identify stretch goals and document them
  - Ejemplo: Calculate, document, and prioritize positive risks alongside negative risks

### GV.RR Roles, Responsibilities, and Authorities

Cybersecurity roles, responsibilities, and authorities to foster accountability, performance assessment, and continuous improvement are established and communicated

- **GV.RR-01**: Organizational leadership is responsible and accountable for cybersecurity risk and fosters a culture that is risk-aware, ethical, and continually improving
  - Ejemplo: Leaders (e.g., directors) agree on their roles and responsibilities in developing, implementing, and assessing the organization's cybersecurity strategy
  - Ejemplo: Share leaders' expectations regarding a secure and ethical culture, especially when current events present the opportunity to highlight positive or negative examples of cybersecurity risk management
  - Ejemplo: Leaders direct the CISO to maintain a comprehensive cybersecurity risk strategy and review and update it at least annually and after major events
  - Ejemplo: Conduct reviews to ensure adequate authority and coordination among those responsible for managing cybersecurity risk
- **GV.RR-02**: Roles, responsibilities, and authorities related to cybersecurity risk management are established, communicated, understood, and enforced
  - Ejemplo: Document risk management roles and responsibilities in policy
  - Ejemplo: Document who is responsible and accountable for cybersecurity risk management activities and how those teams and individuals are to be consulted and informed
  - Ejemplo: Include cybersecurity responsibilities and performance requirements in personnel descriptions
  - Ejemplo: Document performance goals for personnel with cybersecurity risk management responsibilities, and periodically measure performance to identify areas for improvement
  - Ejemplo: Clearly articulate cybersecurity responsibilities within operations, risk functions, and internal audit functions
- **GV.RR-03**: Adequate resources are allocated commensurate with the cybersecurity risk strategy, roles, responsibilities, and policies
  - Ejemplo: Conduct periodic management reviews to ensure that those given cybersecurity risk management responsibilities have the necessary authority
  - Ejemplo: Identify resource allocation and investment in line with risk tolerance and response
  - Ejemplo: Provide adequate and sufficient people, process, and technical resources to support the cybersecurity strategy
- **GV.RR-04**: Cybersecurity is included in human resources practices
  - Ejemplo: Integrate cybersecurity risk management considerations into human resources processes (e.g., personnel screening, onboarding, change notification, offboarding)
  - Ejemplo: Consider cybersecurity knowledge to be a positive factor in hiring, training, and retention decisions
  - Ejemplo: Conduct background checks prior to onboarding new personnel for sensitive roles, and periodically repeat background checks for personnel with such roles
  - Ejemplo: Define and enforce obligations for personnel to be aware of, adhere to, and uphold security policies as they relate to their roles

### GV.PO Policy

Organizational cybersecurity policy is established, communicated, and enforced

- **GV.PO-01**: Policy for managing cybersecurity risks is established based on organizational context, cybersecurity strategy, and priorities and is communicated and enforced
  - Ejemplo: Create, disseminate, and maintain an understandable, usable risk management policy with statements of management intent, expectations, and direction
  - Ejemplo: Periodically review policy and supporting processes and procedures to ensure that they align with risk management strategy objectives and priorities, as well as the high-level direction of the cybersecurity policy
  - Ejemplo: Require approval from senior management on policy
  - Ejemplo: Communicate cybersecurity risk management policy and supporting processes and procedures across the organization
  - Ejemplo: Require personnel to acknowledge receipt of policy when first hired, annually, and whenever policy is updated
- **GV.PO-02**: Policy for managing cybersecurity risks is reviewed, updated, communicated, and enforced to reflect changes in requirements, threats, technology, and organizational mission
  - Ejemplo: Update policy based on periodic reviews of cybersecurity risk management results to ensure that policy and supporting processes and procedures adequately maintain risk at an acceptable level
  - Ejemplo: Provide a timeline for reviewing changes to the organization's risk environment (e.g., changes in risk or in the organization's mission objectives), and communicate recommended policy updates
  - Ejemplo: Update policy to reflect changes in legal and regulatory requirements
  - Ejemplo: Update policy to reflect changes in technology (e.g., adoption of artificial intelligence) and changes to the business (e.g., acquisition of a new business, new contract requirements)

### GV.OV Oversight

Results of organization-wide cybersecurity risk management activities and performance are used to inform, improve, and adjust the risk management strategy

- **GV.OV-01**: Cybersecurity risk management strategy outcomes are reviewed to inform and adjust strategy and direction
  - Ejemplo: Measure how well the risk management strategy and risk results have helped leaders make decisions and achieve organizational objectives
  - Ejemplo: Examine whether cybersecurity risk strategies that impede operations or innovation should be adjusted
- **GV.OV-02**: The cybersecurity risk management strategy is reviewed and adjusted to ensure coverage of organizational requirements and risks
  - Ejemplo: Review audit findings to confirm whether the existing cybersecurity strategy has ensured compliance with internal and external requirements
  - Ejemplo: Review the performance oversight of those in cybersecurity-related roles to determine whether policy changes are necessary
  - Ejemplo: Review strategy in light of cybersecurity incidents
- **GV.OV-03**: Organizational cybersecurity risk management performance is evaluated and reviewed for adjustments needed
  - Ejemplo: Review key performance indicators (KPIs) to ensure that organization-wide policies and procedures achieve objectives
  - Ejemplo: Review key risk indicators (KRIs) to identify risks the organization faces, including likelihood and potential impact
  - Ejemplo: Collect and communicate metrics on cybersecurity risk management with senior leadership

### GV.SC Cybersecurity Supply Chain Risk Management

Cyber supply chain risk management processes are identified, established, managed, monitored, and improved by organizational stakeholders

- **GV.SC-01**: A cybersecurity supply chain risk management program, strategy, objectives, policies, and processes are established and agreed to by organizational stakeholders
  - Ejemplo: Establish a strategy that expresses the objectives of the cybersecurity supply chain risk management program
  - Ejemplo: Develop the cybersecurity supply chain risk management program, including a plan (with milestones), policies, and procedures that guide implementation and improvement of the program, and share the policies and procedures with the organizational stakeholders
  - Ejemplo: Develop and implement program processes based on the strategy, objectives, policies, and procedures that are agreed upon and performed by the organizational stakeholders
  - Ejemplo: Establish a cross-organizational mechanism that ensures alignment between functions that contribute to cybersecurity supply chain risk management, such as cybersecurity, IT, operations, legal, human resources, and engineering
- **GV.SC-02**: Cybersecurity roles and responsibilities for suppliers, customers, and partners are established, communicated, and coordinated internally and externally
  - Ejemplo: Identify one or more specific roles or positions that will be responsible and accountable for planning, resourcing, and executing cybersecurity supply chain risk management activities
  - Ejemplo: Document cybersecurity supply chain risk management roles and responsibilities in policy
  - Ejemplo: Create responsibility matrixes to document who will be responsible and accountable for cybersecurity supply chain risk management activities and how those teams and individuals will be consulted and informed
  - Ejemplo: Include cybersecurity supply chain risk management responsibilities and performance requirements in personnel descriptions to ensure clarity and improve accountability
  - Ejemplo: Document performance goals for personnel with cybersecurity risk management-specific responsibilities, and periodically measure them to demonstrate and improve performance
  - Ejemplo: Develop roles and responsibilities for suppliers, customers, and business partners to address shared responsibilities for applicable cybersecurity risks, and integrate them into organizational policies and applicable third-party agreements
  - Ejemplo: Internally communicate cybersecurity supply chain risk management roles and responsibilities for third parties
  - Ejemplo: Establish rules and protocols for information sharing and reporting processes between the organization and its suppliers
- **GV.SC-03**: Cybersecurity supply chain risk management is integrated into cybersecurity and enterprise risk management, risk assessment, and improvement processes
  - Ejemplo: Identify areas of alignment and overlap with cybersecurity and enterprise risk management
  - Ejemplo: Establish integrated control sets for cybersecurity risk management and cybersecurity supply chain risk management
  - Ejemplo: Integrate cybersecurity supply chain risk management into improvement processes
  - Ejemplo: Escalate material cybersecurity risks in supply chains to senior management, and address them at the enterprise risk management level
- **GV.SC-04**: Suppliers are known and prioritized by criticality
  - Ejemplo: Develop criteria for supplier criticality based on, for example, the sensitivity of data processed or possessed by suppliers, the degree of access to the organization's systems, and the importance of the products or services to the organization's mission
  - Ejemplo: Keep a record of all suppliers, and prioritize suppliers based on the criticality criteria
- **GV.SC-05**: Requirements to address cybersecurity risks in supply chains are established, prioritized, and integrated into contracts and other types of agreements with suppliers and other relevant third parties
  - Ejemplo: Establish security requirements for suppliers, products, and services commensurate with their criticality level and potential impact if compromised
  - Ejemplo: Include all cybersecurity and supply chain requirements that third parties must follow and how compliance with the requirements may be verified in default contractual language
  - Ejemplo: Define the rules and protocols for information sharing between the organization and its suppliers and sub-tier suppliers in agreements
  - Ejemplo: Manage risk by including security requirements in agreements based on their criticality and potential impact if compromised
  - Ejemplo: Define security requirements in service-level agreements (SLAs) for monitoring suppliers for acceptable security performance throughout the supplier relationship lifecycle
  - Ejemplo: Contractually require suppliers to disclose cybersecurity features, functions, and vulnerabilities of their products and services for the life of the product or the term of service
  - Ejemplo: Contractually require suppliers to provide and maintain a current component inventory (e.g., software or hardware bill of materials) for critical products
  - Ejemplo: Contractually require suppliers to vet their employees and guard against insider threats
  - Ejemplo: Contractually require suppliers to provide evidence of performing acceptable security practices through, for example, self-attestation, conformance to known standards, certifications, or inspections
  - Ejemplo: Specify in contracts and other agreements the rights and responsibilities of the organization, its suppliers, and their supply chains, with respect to potential cybersecurity risks
- **GV.SC-06**: Planning and due diligence are performed to reduce risks before entering into formal supplier or other third-party relationships
  - Ejemplo: Perform thorough due diligence on prospective suppliers that is consistent with procurement planning and commensurate with the level of risk, criticality, and complexity of each supplier relationship
  - Ejemplo: Assess the suitability of the technology and cybersecurity capabilities and the risk management practices of prospective suppliers
  - Ejemplo: Conduct supplier risk assessments against business and applicable cybersecurity requirements
  - Ejemplo: Assess the authenticity, integrity, and security of critical products prior to acquisition and use
- **GV.SC-07**: The risks posed by a supplier, their products and services, and other third parties are understood, recorded, prioritized, assessed, responded to, and monitored over the course of the relationship
  - Ejemplo: Adjust assessment formats and frequencies based on the third party's reputation and the criticality of the products or services they provide
  - Ejemplo: Evaluate third parties' evidence of compliance with contractual cybersecurity requirements, such as self-attestations, warranties, certifications, and other artifacts
  - Ejemplo: Monitor critical suppliers to ensure that they are fulfilling their security obligations throughout the supplier relationship lifecycle using a variety of methods and techniques, such as inspections, audits, tests, or other forms of evaluation
  - Ejemplo: Monitor critical suppliers, services, and products for changes to their risk profiles, and reevaluate supplier criticality and risk impact accordingly
  - Ejemplo: Plan for unexpected supplier and supply chain-related interruptions to ensure business continuity
- **GV.SC-08**: Relevant suppliers and other third parties are included in incident planning, response, and recovery activities
  - Ejemplo: Define and use rules and protocols for reporting incident response and recovery activities and the status between the organization and its suppliers
  - Ejemplo: Identify and document the roles and responsibilities of the organization and its suppliers for incident response
  - Ejemplo: Include critical suppliers in incident response exercises and simulations
  - Ejemplo: Define and coordinate crisis communication methods and protocols between the organization and its critical suppliers
  - Ejemplo: Conduct collaborative lessons learned sessions with critical suppliers
- **GV.SC-09**: Supply chain security practices are integrated into cybersecurity and enterprise risk management programs, and their performance is monitored throughout the technology product and service life cycle
  - Ejemplo: Policies and procedures require provenance records for all acquired technology products and services
  - Ejemplo: Periodically provide risk reporting to leaders about how acquired components are proven to be untampered and authentic
  - Ejemplo: Communicate regularly among cybersecurity risk managers and operations personnel about the need to acquire software patches, updates, and upgrades only from authenticated and trustworthy software providers
  - Ejemplo: Review policies to ensure that they require approved supplier personnel to perform maintenance on supplier products
  - Ejemplo: Policies and procedure require checking upgrades to critical hardware for unauthorized changes
- **GV.SC-10**: Cybersecurity supply chain risk management plans include provisions for activities that occur after the conclusion of a partnership or service agreement
  - Ejemplo: Establish processes for terminating critical relationships under both normal and adverse circumstances
  - Ejemplo: Define and implement plans for component end-of-life maintenance support and obsolescence
  - Ejemplo: Verify that supplier access to organization resources is deactivated promptly when it is no longer needed
  - Ejemplo: Verify that assets containing the organization's data are returned or properly disposed of in a timely, controlled, and safe manner
  - Ejemplo: Develop and execute a plan for terminating or transitioning supplier relationships that takes supply chain security risk and resiliency into account
  - Ejemplo: Mitigate risks to data and systems created by supplier termination
  - Ejemplo: Manage data leakage risks associated with supplier termination

## ID IDENTIFY

The organization's current cybersecurity risks are understood

### ID.AM Asset Management

Assets (e.g., data, hardware, software, systems, facilities, services, people) that enable the organization to achieve business purposes are identified and managed consistent with their relative importance to organizational objectives and the organization's risk strategy

- **ID.AM-01**: Inventories of hardware managed by the organization are maintained
  - Ejemplo: Maintain inventories for all types of hardware, including IT, IoT, OT, and mobile devices
  - Ejemplo: Constantly monitor networks to detect new hardware and automatically update inventories
- **ID.AM-02**: Inventories of software, services, and systems managed by the organization are maintained
  - Ejemplo: Maintain inventories for all types of software and services, including commercial-off-the-shelf, open-source, custom applications, API services, and cloud-based applications and services
  - Ejemplo: Constantly monitor all platforms, including containers and virtual machines, for software and service inventory changes
  - Ejemplo: Maintain an inventory of the organization's systems
- **ID.AM-03**: Representations of the organization's authorized network communication and internal and external network data flows are maintained
  - Ejemplo: Maintain baselines of communication and data flows within the organization's wired and wireless networks
  - Ejemplo: Maintain baselines of communication and data flows between the organization and third parties
  - Ejemplo: Maintain baselines of communication and data flows for the organization's infrastructure-as-a-service (IaaS) usage
  - Ejemplo: Maintain documentation of expected network ports, protocols, and services that are typically used among authorized systems
- **ID.AM-04**: Inventories of services provided by suppliers are maintained
  - Ejemplo: Inventory all external services used by the organization, including third-party infrastructure-as-a-service (IaaS), platform-as-a-service (PaaS), and software-as-a-service (SaaS) offerings; APIs; and other externally hosted application services
  - Ejemplo: Update the inventory when a new external service is going to be utilized to ensure adequate cybersecurity risk management monitoring of the organization's use of that service
- **ID.AM-05**: Assets are prioritized based on classification, criticality, resources, and impact on the mission
  - Ejemplo: Define criteria for prioritizing each class of assets
  - Ejemplo: Apply the prioritization criteria to assets
  - Ejemplo: Track the asset priorities and update them periodically or when significant changes to the organization occur
- **ID.AM-07**: Inventories of data and corresponding metadata for designated data types are maintained
  - Ejemplo: Maintain a list of the designated data types of interest (e.g., personally identifiable information, protected health information, financial account numbers, organization intellectual property, operational technology data)
  - Ejemplo: Continuously discover and analyze ad hoc data to identify new instances of designated data types
  - Ejemplo: Assign data classifications to designated data types through tags or labels
  - Ejemplo: Track the provenance, data owner, and geolocation of each instance of designated data types
- **ID.AM-08**: Systems, hardware, software, services, and data are managed throughout their life cycles
  - Ejemplo: Integrate cybersecurity considerations throughout the life cycles of systems, hardware, software, and services
  - Ejemplo: Integrate cybersecurity considerations into product life cycles
  - Ejemplo: Identify unofficial uses of technology to meet mission objectives (i.e., shadow IT)
  - Ejemplo: Periodically identify redundant systems, hardware, software, and services that unnecessarily increase the organization's attack surface
  - Ejemplo: Properly configure and secure systems, hardware, software, and services prior to their deployment in production
  - Ejemplo: Update inventories when systems, hardware, software, and services are moved or transferred within the organization
  - Ejemplo: Securely destroy stored data based on the organization's data retention policy using the prescribed destruction method, and keep and manage a record of the destructions
  - Ejemplo: Securely sanitize data storage when hardware is being retired, decommissioned, reassigned, or sent for repairs or replacement
  - Ejemplo: Offer methods for destroying paper, storage media, and other physical forms of data storage

### ID.RA Risk Assessment

The cybersecurity risk to the organization, assets, and individuals is understood by the organization

- **ID.RA-01**: Vulnerabilities in assets are identified, validated, and recorded
  - Ejemplo: Use vulnerability management technologies to identify unpatched and misconfigured software
  - Ejemplo: Assess network and system architectures for design and implementation weaknesses that affect cybersecurity
  - Ejemplo: Review, analyze, or test organization-developed software to identify design, coding, and default configuration vulnerabilities
  - Ejemplo: Assess facilities that house critical computing assets for physical vulnerabilities and resilience issues
  - Ejemplo: Monitor sources of cyber threat intelligence for information on new vulnerabilities in products and services
  - Ejemplo: Review processes and procedures for weaknesses that could be exploited to affect cybersecurity
- **ID.RA-02**: Cyber threat intelligence is received from information sharing forums and sources
  - Ejemplo: Configure cybersecurity tools and technologies with detection or response capabilities to securely ingest cyber threat intelligence feeds
  - Ejemplo: Receive and review advisories from reputable third parties on current threat actors and their tactics, techniques, and procedures (TTPs)
  - Ejemplo: Monitor sources of cyber threat intelligence for information on the types of vulnerabilities that emerging technologies may have
- **ID.RA-03**: Internal and external threats to the organization are identified and recorded
  - Ejemplo: Use cyber threat intelligence to maintain awareness of the types of threat actors likely to target the organization and the TTPs they are likely to use
  - Ejemplo: Perform threat hunting to look for signs of threat actors within the environment
  - Ejemplo: Implement processes for identifying internal threat actors
- **ID.RA-04**: Potential impacts and likelihoods of threats exploiting vulnerabilities are identified and recorded
  - Ejemplo: Business leaders and cybersecurity risk management practitioners work together to estimate the likelihood and impact of risk scenarios and record them in risk registers
  - Ejemplo: Enumerate the potential business impacts of unauthorized access to the organization's communications, systems, and data processed in or by those systems
  - Ejemplo: Account for the potential impacts of cascading failures for systems of systems
- **ID.RA-05**: Threats, vulnerabilities, likelihoods, and impacts are used to understand inherent risk and inform risk response prioritization
  - Ejemplo: Develop threat models to better understand risks to the data and identify appropriate risk responses
  - Ejemplo: Prioritize cybersecurity resource allocations and investments based on estimated likelihoods and impacts
- **ID.RA-06**: Risk responses are chosen, prioritized, planned, tracked, and communicated
  - Ejemplo: Apply the vulnerability management plan's criteria for deciding whether to accept, transfer, mitigate, or avoid risk
  - Ejemplo: Apply the vulnerability management plan's criteria for selecting compensating controls to mitigate risk
  - Ejemplo: Track the progress of risk response implementation (e.g., plan of action and milestones [POA&M], risk register, risk detail report)
  - Ejemplo: Use risk assessment findings to inform risk response decisions and actions
  - Ejemplo: Communicate planned risk responses to affected stakeholders in priority order
- **ID.RA-07**: Changes and exceptions are managed, assessed for risk impact, recorded, and tracked
  - Ejemplo: Implement and follow procedures for the formal documentation, review, testing, and approval of proposed changes and requested exceptions
  - Ejemplo: Document the possible risks of making or not making each proposed change, and provide guidance on rolling back changes
  - Ejemplo: Document the risks related to each requested exception and the plan for responding to those risks
  - Ejemplo: Periodically review risks that were accepted based upon planned future actions or milestones
- **ID.RA-08**: Processes for receiving, analyzing, and responding to vulnerability disclosures are established
  - Ejemplo: Conduct vulnerability information sharing between the organization and its suppliers following the rules and protocols defined in contracts
  - Ejemplo: Assign responsibilities and verify the execution of procedures for processing, analyzing the impact of, and responding to cybersecurity threat, vulnerability, or incident disclosures by suppliers, customers, partners, and government cybersecurity organizations
- **ID.RA-09**: The authenticity and integrity of hardware and software are assessed prior to acquisition and use
  - Ejemplo: Assess the authenticity and cybersecurity of critical technology products and services prior to acquisition and use
- **ID.RA-10**: Critical suppliers are assessed prior to acquisition
  - Ejemplo: Conduct supplier risk assessments against business and applicable cybersecurity requirements, including the supply chain

### ID.IM Improvement

Improvements to organizational cybersecurity risk management processes, procedures and activities are identified across all CSF Functions

- **ID.IM-01**: Improvements are identified from evaluations
  - Ejemplo: Perform self-assessments of critical services that take current threats and TTPs into consideration
  - Ejemplo: Invest in third-party assessments or independent audits of the effectiveness of the organization's cybersecurity program to identify areas that need improvement
  - Ejemplo: Constantly evaluate compliance with selected cybersecurity requirements through automated means
- **ID.IM-02**: Improvements are identified from security tests and exercises, including those done in coordination with suppliers and relevant third parties
  - Ejemplo: Identify improvements for future incident response activities based on findings from incident response assessments (e.g., tabletop exercises and simulations, tests, internal reviews, independent audits)
  - Ejemplo: Identify improvements for future business continuity, disaster recovery, and incident response activities based on exercises performed in coordination with critical service providers and product suppliers
  - Ejemplo: Involve internal stakeholders (e.g., senior executives, legal department, HR) in security tests and exercises as appropriate
  - Ejemplo: Perform penetration testing to identify opportunities to improve the security posture of selected high-risk systems as approved by leadership
  - Ejemplo: Exercise contingency plans for responding to and recovering from the discovery that products or services did not originate with the contracted supplier or partner or were altered before receipt
  - Ejemplo: Collect and analyze performance metrics using security tools and services to inform improvements to the cybersecurity program
- **ID.IM-03**: Improvements are identified from execution of operational processes, procedures, and activities
  - Ejemplo: Conduct collaborative lessons learned sessions with suppliers
  - Ejemplo: Annually review cybersecurity policies, processes, and procedures to take lessons learned into account
  - Ejemplo: Use metrics to assess operational cybersecurity performance over time
- **ID.IM-04**: Incident response plans and other cybersecurity plans that affect operations are established, communicated, maintained, and improved
  - Ejemplo: Establish contingency plans (e.g., incident response, business continuity, disaster recovery) for responding to and recovering from adverse events that can interfere with operations, expose confidential information, or otherwise endanger the organization's mission and viability
  - Ejemplo: Include contact and communication information, processes for handling common scenarios, and criteria for prioritization, escalation, and elevation in all contingency plans
  - Ejemplo: Create a vulnerability management plan to identify and assess all types of vulnerabilities and to prioritize, test, and implement risk responses
  - Ejemplo: Communicate cybersecurity plans (including updates) to those responsible for carrying them out and to affected parties
  - Ejemplo: Review and update all cybersecurity plans annually or when a need for significant improvements is identified

## PR PROTECT

Safeguards to manage the organization's cybersecurity risks are used

### PR.AA Identity Management, Authentication, and Access Control

Access to physical and logical assets is limited to authorized users, services, and hardware and  managed commensurate with the assessed risk of unauthorized access

- **PR.AA-01**: Identities and credentials for authorized users, services, and hardware are managed by the organization
  - Ejemplo: Initiate requests for new access or additional access for employees, contractors, and others, and track, review, and fulfill the requests, with permission from system or data owners when needed
  - Ejemplo: Issue, manage, and revoke cryptographic certificates and identity tokens, cryptographic keys (i.e., key management), and other credentials
  - Ejemplo: Select a unique identifier for each device from immutable hardware characteristics or an identifier securely provisioned to the device
  - Ejemplo: Physically label authorized hardware with an identifier for inventory and servicing purposes
- **PR.AA-02**: Identities are proofed and bound to credentials based on the context of interactions
  - Ejemplo: Verify a person's claimed identity at enrollment time using government-issued identity credentials (e.g., passport, visa, driver's license)
  - Ejemplo: Issue a different credential for each person (i.e., no credential sharing)
- **PR.AA-03**: Users, services, and hardware are authenticated
  - Ejemplo: Require multifactor authentication
  - Ejemplo: Enforce policies for the minimum strength of passwords, PINs, and similar authenticators
  - Ejemplo: Periodically reauthenticate users, services, and hardware based on risk (e.g., in zero trust architectures)
  - Ejemplo: Ensure that authorized personnel can access accounts essential for protecting safety under emergency conditions
- **PR.AA-04**: Identity assertions are protected, conveyed, and verified
  - Ejemplo: Protect identity assertions that are used to convey authentication and user information through single sign-on systems
  - Ejemplo: Protect identity assertions that are used to convey authentication and user information between federated systems
  - Ejemplo: Implement standards-based approaches for identity assertions in all contexts, and follow all guidance for the generation (e.g., data models, metadata), protection (e.g., digital signing, encryption), and verification (e.g., signature validation) of identity assertions
- **PR.AA-05**: Access permissions, entitlements, and authorizations are defined in a policy, managed, enforced, and reviewed, and incorporate the principles of least privilege and separation of duties
  - Ejemplo: Review logical and physical access privileges periodically and whenever someone changes roles or leaves the organization, and promptly rescind privileges that are no longer needed
  - Ejemplo: Take attributes of the requester and the requested resource into account for authorization decisions (e.g., geolocation, day/time, requester endpoint's cyber health)
  - Ejemplo: Restrict access and privileges to the minimum necessary (e.g., zero trust architecture)
  - Ejemplo: Periodically review the privileges associated with critical business functions to confirm proper separation of duties
- **PR.AA-06**: Physical access to assets is managed, monitored, and enforced commensurate with risk
  - Ejemplo: Use security guards, security cameras, locked entrances, alarm systems, and other physical controls to monitor facilities and restrict access
  - Ejemplo: Employ additional physical security controls for areas that contain high-risk assets
  - Ejemplo: Escort guests, vendors, and other third parties within areas that contain business-critical assets

### PR.AT Awareness and Training

The organization's personnel are provided with cybersecurity awareness and training so that they can perform their cybersecurity-related tasks

- **PR.AT-01**: Personnel are provided with awareness and training so that they possess the knowledge and skills to perform general tasks with cybersecurity risks in mind
  - Ejemplo: Provide basic cybersecurity awareness and training to employees, contractors, partners, suppliers, and all other users of the organization's non-public resources
  - Ejemplo: Train personnel to recognize social engineering attempts and other common attacks, report attacks and suspicious activity, comply with acceptable use policies, and perform basic cyber hygiene tasks (e.g., patching software, choosing passwords, protecting credentials)
  - Ejemplo: Explain the consequences of cybersecurity policy violations, both to individual users and the organization as a whole
  - Ejemplo: Periodically assess or test users on their understanding of basic cybersecurity practices
  - Ejemplo: Require annual refreshers to reinforce existing practices and introduce new practices
- **PR.AT-02**: Individuals in specialized roles are provided with awareness and training so that they possess the knowledge and skills to perform relevant tasks with cybersecurity risks in mind
  - Ejemplo: Identify the specialized roles within the organization that require additional cybersecurity training, such as physical and cybersecurity personnel, finance personnel, senior leadership, and anyone with access to business-critical data
  - Ejemplo: Provide role-based cybersecurity awareness and training to all those in specialized roles, including contractors, partners, suppliers, and other third parties
  - Ejemplo: Periodically assess or test users on their understanding of cybersecurity practices for their specialized roles
  - Ejemplo: Require annual refreshers to reinforce existing practices and introduce new practices

### PR.DS Data Security

Data are managed consistent with the organization's risk strategy to protect the confidentiality, integrity, and availability of information

- **PR.DS-01**: The confidentiality, integrity, and availability of data-at-rest are protected
  - Ejemplo: Use encryption, digital signatures, and cryptographic hashes to protect the confidentiality and integrity of stored data in files, databases, virtual machine disk images, container images, and other resources
  - Ejemplo: Use full disk encryption to protect data stored on user endpoints
  - Ejemplo: Confirm the integrity of software by validating signatures
  - Ejemplo: Restrict the use of removable media to prevent data exfiltration
  - Ejemplo: Physically secure removable media containing unencrypted sensitive information, such as within locked offices or file cabinets
- **PR.DS-02**: The confidentiality, integrity, and availability of data-in-transit are protected
  - Ejemplo: Use encryption, digital signatures, and cryptographic hashes to protect the confidentiality and integrity of network communications
  - Ejemplo: Automatically encrypt or block outbound emails and other communications that contain sensitive data, depending on the data classification
  - Ejemplo: Block access to personal email, file sharing, file storage services, and other personal communications applications and services from organizational systems and networks
  - Ejemplo: Prevent reuse of sensitive data from production environments (e.g., customer records) in development, testing, and other non-production environments
- **PR.DS-10**: The confidentiality, integrity, and availability of data-in-use are protected
  - Ejemplo: Remove data that must remain confidential (e.g., from processors and memory) as soon as it is no longer needed
  - Ejemplo: Protect data in use from access by other users and processes of the same platform
- **PR.DS-11**: Backups of data are created, protected, maintained, and tested
  - Ejemplo: Continuously back up critical data in near-real-time, and back up other data frequently at agreed-upon schedules
  - Ejemplo: Test backups and restores for all types of data sources at least annually
  - Ejemplo: Securely store some backups offline and offsite so that an incident or disaster will not damage them
  - Ejemplo: Enforce geographic separation and geolocation restrictions for data backup storage

### PR.PS Platform Security

The hardware, software (e.g., firmware, operating systems, applications), and services of physical and virtual platforms are managed consistent with the organization's risk strategy to protect their confidentiality, integrity, and availability

- **PR.PS-01**: Configuration management practices are established and applied
  - Ejemplo: Establish, test, deploy, and maintain hardened baselines that enforce the organization's cybersecurity policies and provide only essential capabilities (i.e., principle of least functionality)
  - Ejemplo: Review all default configuration settings that may potentially impact cybersecurity when installing or upgrading software
  - Ejemplo: Monitor implemented software for deviations from approved baselines
- **PR.PS-02**: Software is maintained, replaced, and removed commensurate with risk
  - Ejemplo: Perform routine and emergency patching within the timeframes specified in the vulnerability management plan
  - Ejemplo: Update container images, and deploy new container instances to replace rather than update existing instances
  - Ejemplo: Replace end-of-life software and service versions with supported, maintained versions
  - Ejemplo: Uninstall and remove unauthorized software and services that pose undue risks
  - Ejemplo: Uninstall and remove any unnecessary software components (e.g., operating system utilities) that attackers might misuse
  - Ejemplo: Define and implement plans for software and service end-of-life maintenance support and obsolescence
- **PR.PS-03**: Hardware is maintained, replaced, and removed commensurate with risk
  - Ejemplo: Replace hardware when it lacks needed security capabilities or when it cannot support software with needed security capabilities
  - Ejemplo: Define and implement plans for hardware end-of-life maintenance support and obsolescence
  - Ejemplo: Perform hardware disposal in a secure, responsible, and auditable manner
- **PR.PS-04**: Log records are generated and made available for continuous monitoring
  - Ejemplo: Configure all operating systems, applications, and services (including cloud-based services) to generate log records
  - Ejemplo: Configure log generators to securely share their logs with the organization's logging infrastructure systems and services
  - Ejemplo: Configure log generators to record the data needed by zero-trust architectures
- **PR.PS-05**: Installation and execution of unauthorized software are prevented
  - Ejemplo: When risk warrants it, restrict software execution to permitted products only or deny the execution of prohibited and unauthorized software
  - Ejemplo: Verify the source of new software and the software's integrity before installing it
  - Ejemplo: Configure platforms to use only approved DNS services that block access to known malicious domains
  - Ejemplo: Configure platforms to allow the installation of organization-approved software only
- **PR.PS-06**: Secure software development practices are integrated, and their performance is monitored throughout the software development life cycle
  - Ejemplo: Protect all components of organization-developed software from tampering and unauthorized access
  - Ejemplo: Secure all software produced by the organization, with minimal vulnerabilities in their releases
  - Ejemplo: Maintain the software used in production environments, and securely dispose of software once it is no longer needed

### PR.IR Technology Infrastructure Resilience

Security architectures are managed with the organization's risk strategy to protect asset confidentiality, integrity, and availability, and organizational resilience

- **PR.IR-01**: Networks and environments are protected from unauthorized logical access and usage
  - Ejemplo: Logically segment organization networks and cloud-based platforms according to trust boundaries and platform types (e.g., IT, IoT, OT, mobile, guests), and permit required communications only between segments
  - Ejemplo: Logically segment organization networks from external networks, and permit only necessary communications to enter the organization's networks from the external networks
  - Ejemplo: Implement zero trust architectures to restrict network access to each resource to the minimum necessary
  - Ejemplo: Check the cyber health of endpoints before allowing them to access and use production resources
- **PR.IR-02**: The organization's technology assets are protected from environmental threats
  - Ejemplo: Protect organizational equipment from known environmental threats, such as flooding, fire, wind, and excessive heat and humidity
  - Ejemplo: Include protection from environmental threats and provisions for adequate operating infrastructure in requirements for service providers that operate systems on the organization's behalf
- **PR.IR-03**: Mechanisms are implemented to achieve resilience requirements in normal and adverse situations
  - Ejemplo: Avoid single points of failure in systems and infrastructure
  - Ejemplo: Use load balancing to increase capacity and improve reliability
  - Ejemplo: Use high-availability components like redundant storage and power supplies to improve system reliability
- **PR.IR-04**: Adequate resource capacity to ensure availability is maintained
  - Ejemplo: Monitor usage of storage, power, compute, network bandwidth, and other resources
  - Ejemplo: Forecast future needs, and scale resources accordingly

## DE DETECT

Possible cybersecurity attacks and compromises are found and analyzed

### DE.AE Adverse Event Analysis

Anomalies, indicators of compromise, and other potentially adverse events are analyzed to characterize the events and detect cybersecurity incidents

- **DE.AE-02**: Potentially adverse events are analyzed to better understand associated activities
  - Ejemplo: Use security information and event management (SIEM) or other tools to continuously monitor log events for known malicious and suspicious activity
  - Ejemplo: Utilize up-to-date cyber threat intelligence in log analysis tools to improve detection accuracy and characterize threat actors, their methods, and indicators of compromise
  - Ejemplo: Regularly conduct manual reviews of log events for technologies that cannot be sufficiently monitored through automation
  - Ejemplo: Use log analysis tools to generate reports on their findings
- **DE.AE-03**: Information is correlated from multiple sources
  - Ejemplo: Constantly transfer log data generated by other sources to a relatively small number of log servers
  - Ejemplo: Use event correlation technology (e.g., SIEM) to collect information captured by multiple sources
  - Ejemplo: Utilize cyber threat intelligence to help correlate events among log sources
- **DE.AE-04**: The estimated impact and scope of adverse events are understood
  - Ejemplo: Use SIEMs or other tools to estimate impact and scope, and review and refine the estimates
  - Ejemplo: A person creates their own estimates of impact and scope
- **DE.AE-06**: Information on adverse events is provided to authorized staff and tools
  - Ejemplo: Use cybersecurity software to generate alerts and provide them to the security operations center (SOC), incident responders, and incident response tools
  - Ejemplo: Incident responders and other authorized personnel can access log analysis findings at all times
  - Ejemplo: Automatically create and assign tickets in the organization's ticketing system when certain types of alerts occur
  - Ejemplo: Manually create and assign tickets in the organization's ticketing system when technical staff discover indicators of compromise
- **DE.AE-07**: Cyber threat intelligence and other contextual information are integrated into the analysis
  - Ejemplo: Securely provide cyber threat intelligence feeds to detection technologies, processes, and personnel
  - Ejemplo: Securely provide information from asset inventories to detection technologies, processes, and personnel
  - Ejemplo: Rapidly acquire and analyze vulnerability disclosures for the organization's technologies from suppliers, vendors, and third-party security advisories
- **DE.AE-08**: Incidents are declared when adverse events meet the defined incident criteria
  - Ejemplo: Apply incident criteria to known and assumed characteristics of activity in order to determine whether an incident should be declared
  - Ejemplo: Take known false positives into account when applying incident criteria

### DE.CM Continuous Monitoring

Assets are monitored to find anomalies, indicators of compromise, and other potentially adverse events

- **DE.CM-01**: Networks and network services are monitored to find potentially adverse events
  - Ejemplo: Monitor DNS, BGP, and other network services for adverse events
  - Ejemplo: Monitor wired and wireless networks for connections from unauthorized endpoints
  - Ejemplo: Monitor facilities for unauthorized or rogue wireless networks
  - Ejemplo: Compare actual network flows against baselines to detect deviations
  - Ejemplo: Monitor network communications to identify changes in security postures for zero trust purposes
- **DE.CM-02**: The physical environment is monitored to find potentially adverse events
  - Ejemplo: Monitor logs from physical access control systems (e.g., badge readers) to find unusual access patterns (e.g., deviations from the norm) and failed access attempts
  - Ejemplo: Review and monitor physical access records (e.g., from visitor registration, sign-in sheets)
  - Ejemplo: Monitor physical access controls (e.g., locks, latches, hinge pins, alarms) for signs of tampering
  - Ejemplo: Monitor the physical environment using alarm systems, cameras, and security guards
- **DE.CM-03**: Personnel activity and technology usage are monitored to find potentially adverse events
  - Ejemplo: Use behavior analytics software to detect anomalous user activity to mitigate insider threats
  - Ejemplo: Monitor logs from logical access control systems to find unusual access patterns and failed access attempts
  - Ejemplo: Continuously monitor deception technology, including user accounts, for any usage
- **DE.CM-06**: External service provider activities and services are monitored to find potentially adverse events
  - Ejemplo: Monitor remote and onsite administration and maintenance activities that external providers perform on organizational systems
  - Ejemplo: Monitor activity from cloud-based services, internet service providers, and other service providers for deviations from expected behavior
- **DE.CM-09**: Computing hardware and software, runtime environments, and their data are monitored to find potentially adverse events
  - Ejemplo: Monitor email, web, file sharing, collaboration services, and other common attack vectors to detect malware, phishing, data leaks and exfiltration, and other adverse events
  - Ejemplo: Monitor authentication attempts to identify attacks against credentials and unauthorized credential reuse
  - Ejemplo: Monitor software configurations for deviations from security baselines
  - Ejemplo: Monitor hardware and software for signs of tampering
  - Ejemplo: Use technologies with a presence on endpoints to detect cyber health issues (e.g., missing patches, malware infections, unauthorized software), and redirect the endpoints to a remediation environment before access is authorized

## RS RESPOND

Actions regarding a detected cybersecurity incident are taken

### RS.MA Incident Management

Responses to detected cybersecurity incidents are managed

- **RS.MA-01**: The incident response plan is executed in coordination with relevant third parties once an incident is declared
  - Ejemplo: Detection technologies automatically report confirmed incidents
  - Ejemplo: Request incident response assistance from the organization's incident response outsourcer
  - Ejemplo: Designate an incident lead for each incident
  - Ejemplo: Initiate execution of additional cybersecurity plans as needed to support incident response (for example, business continuity and disaster recovery)
- **RS.MA-02**: Incident reports are triaged and validated
  - Ejemplo: Preliminarily review incident reports to confirm that they are cybersecurity-related and necessitate incident response activities
  - Ejemplo: Apply criteria to estimate the severity of an incident
- **RS.MA-03**: Incidents are categorized and prioritized
  - Ejemplo: Further review and categorize incidents based on the type of incident (e.g., data breach, ransomware, DDoS, account compromise)
  - Ejemplo: Prioritize incidents based on their scope, likely impact, and time-critical nature
  - Ejemplo: Select incident response strategies for active incidents by balancing the need to quickly recover from an incident with the need to observe the attacker or conduct a more thorough investigation
- **RS.MA-04**: Incidents are escalated or elevated as needed
  - Ejemplo: Track and validate the status of all ongoing incidents
  - Ejemplo: Coordinate incident escalation or elevation with designated internal and external stakeholders
- **RS.MA-05**: The criteria for initiating incident recovery are applied
  - Ejemplo: Apply incident recovery criteria to known and assumed characteristics of the incident to determine whether incident recovery processes should be initiated
  - Ejemplo: Take the possible operational disruption of incident recovery activities into account

### RS.AN Incident Analysis

Investigations are conducted to ensure effective response and support forensics and recovery activities

- **RS.AN-03**: Analysis is performed to establish what has taken place during an incident and the root cause of the incident
  - Ejemplo: Determine the sequence of events that occurred during the incident and which assets and resources were involved in each event
  - Ejemplo: Attempt to determine what vulnerabilities, threats, and threat actors were directly or indirectly involved in the incident
  - Ejemplo: Analyze the incident to find the underlying, systemic root causes
  - Ejemplo: Check any cyber deception technology for additional information on attacker behavior
- **RS.AN-06**: Actions performed during an investigation are recorded, and the records' integrity and provenance are preserved
  - Ejemplo: Require each incident responder and others (e.g., system administrators, cybersecurity engineers) who perform incident response tasks to record their actions and make the record immutable
  - Ejemplo: Require the incident lead to document the incident in detail and be responsible for preserving the integrity of the documentation and the sources of all information being reported
- **RS.AN-07**: Incident data and metadata are collected, and their integrity and provenance are preserved
  - Ejemplo: Collect, preserve, and safeguard the integrity of all pertinent incident data and metadata (e.g., data source, date/time of collection) based on evidence preservation and chain-of-custody procedures
- **RS.AN-08**: An incident's magnitude is estimated and validated
  - Ejemplo: Review other potential targets of the incident to search for indicators of compromise and evidence of persistence
  - Ejemplo: Automatically run tools on targets to look for indicators of compromise and evidence of persistence

### RS.CO Incident Response Reporting and Communication

Response activities are coordinated with internal and external stakeholders as required by laws, regulations, or policies

- **RS.CO-02**: Internal and external stakeholders are notified of incidents
  - Ejemplo: Follow the organization's breach notification procedures after discovering a data breach incident, including notifying affected customers
  - Ejemplo: Notify business partners and customers of incidents in accordance with contractual requirements
  - Ejemplo: Notify law enforcement agencies and regulatory bodies of incidents based on criteria in the incident response plan and management approval
- **RS.CO-03**: Information is shared with designated internal and external stakeholders
  - Ejemplo: Securely share information consistent with response plans and information sharing agreements
  - Ejemplo: Voluntarily share information about an attacker's observed TTPs, with all sensitive data removed, with an Information Sharing and Analysis Center (ISAC)
  - Ejemplo: Notify HR when malicious insider activity occurs
  - Ejemplo: Regularly update senior leadership on the status of major incidents
  - Ejemplo: Follow the rules and protocols defined in contracts for incident information sharing between the organization and its suppliers
  - Ejemplo: Coordinate crisis communication methods between the organization and its critical suppliers

### RS.MI Incident Mitigation

Activities are performed to prevent expansion of an event and mitigate its effects

- **RS.MI-01**: Incidents are contained
  - Ejemplo: Cybersecurity technologies (e.g., antivirus software) and cybersecurity features of other technologies (e.g., operating systems, network infrastructure devices) automatically perform containment actions
  - Ejemplo: Allow incident responders to manually select and perform containment actions
  - Ejemplo: Allow a third party (e.g., internet service provider, managed security service provider) to perform containment actions on behalf of the organization
  - Ejemplo: Automatically transfer compromised endpoints to a remediation virtual local area network (VLAN)
- **RS.MI-02**: Incidents are eradicated
  - Ejemplo: Cybersecurity technologies and cybersecurity features of other technologies (e.g., operating systems, network infrastructure devices) automatically perform eradication actions
  - Ejemplo: Allow incident responders to manually select and perform eradication actions
  - Ejemplo: Allow a third party (e.g., managed security service provider) to perform eradication actions on behalf of the organization

## RC RECOVER

Assets and operations affected by a cybersecurity incident are restored

### RC.RP Incident Recovery Plan Execution

Restoration activities are performed to ensure operational availability of systems and services affected by cybersecurity incidents

- **RC.RP-01**: The recovery portion of the incident response plan is executed once initiated from the incident response process
  - Ejemplo: Begin recovery procedures during or after incident response processes
  - Ejemplo: Make all individuals with recovery responsibilities aware of the plans for recovery and the authorizations required to implement each aspect of the plans
- **RC.RP-02**: Recovery actions are selected, scoped, prioritized, and performed
  - Ejemplo: Select recovery actions based on the criteria defined in the incident response plan and available resources
  - Ejemplo: Change planned recovery actions based on a reassessment of organizational needs and resources
- **RC.RP-03**: The integrity of backups and other restoration assets is verified before using them for restoration
  - Ejemplo: Check restoration assets for indicators of compromise, file corruption, and other integrity issues before use
- **RC.RP-04**: Critical mission functions and cybersecurity risk management are considered to establish post-incident operational norms
  - Ejemplo: Use business impact and system categorization records (including service delivery objectives) to validate that essential services are restored in the appropriate order
  - Ejemplo: Work with system owners to confirm the successful restoration of systems and the return to normal operations
  - Ejemplo: Monitor the performance of restored systems to verify the adequacy of the restoration
- **RC.RP-05**: The integrity of restored assets is verified, systems and services are restored, and normal operating status is confirmed
  - Ejemplo: Check restored assets for indicators of compromise and remediation of root causes of the incident before production use
  - Ejemplo: Verify the correctness and adequacy of the restoration actions taken before putting a restored system online
- **RC.RP-06**: The end of incident recovery is declared based on criteria, and incident-related documentation is completed
  - Ejemplo: Prepare an after-action report that documents the incident itself, the response and recovery actions taken, and lessons learned
  - Ejemplo: Declare the end of incident recovery once the criteria are met

### RC.CO Incident Recovery Communication

Restoration activities are coordinated with internal and external parties

- **RC.CO-03**: Recovery activities and progress in restoring operational capabilities are communicated to designated internal and external stakeholders
  - Ejemplo: Securely share recovery information, including restoration progress, consistent with response plans and information sharing agreements
  - Ejemplo: Regularly update senior leadership on recovery status and restoration progress for major incidents
  - Ejemplo: Follow the rules and protocols defined in contracts for incident information sharing between the organization and its suppliers
  - Ejemplo: Coordinate crisis communication between the organization and its critical suppliers
- **RC.CO-04**: Public updates on incident recovery are shared using approved methods and messaging
  - Ejemplo: Follow the organization's breach notification procedures for recovering from a data breach incident
  - Ejemplo: Explain the steps being taken to recover from the incident and to prevent a recurrence

