# Apple documentation review

Last reviewed with Xcode DocumentationSearch: **2026-08-30**.

Scope: PackageDescription products, targets, platforms, dependencies, resources, binary targets/checksums; Swift availability, Codable, and Sendable.

Fresh queries used for this review:

- `testTarget packageAccess default true SwiftLanguageMode defaultIsolation target binary plugin system library supported platforms minimum deployment Bundle.module resources`
- `PackageDescription external fixture dependency resolution Package.resolved local path Git tag`
- `PackageDescription Target TargetType regular executable test system binary plugin macro target enumeration cases`

## Consulted documentation

- `/documentation/PackageDescription/Product`
- `/documentation/PackageDescription/Product#Creating-a-Library-Product`
- `/documentation/PackageDescription/Product/library(name:type:targets:)`
- `/documentation/PackageDescription/Target`
- `/documentation/PackageDescription/Target#Creating-a-Regular-Target`
- `/documentation/PackageDescription/Target#Creating-a-Test-Target`
- `/documentation/PackageDescription/Target#Creating-a-Plugin-Target`
- `/documentation/PackageDescription/Target#Creating-a-System-Library-Target`
- `/documentation/PackageDescription/Target/testTarget(name:dependencies:path:exclude:sources:resources:packageAccess:cSettings:cxxSettings:swiftSettings:linkerSettings:plugins:)`
- `/documentation/PackageDescription/Target/TargetType#Enumeration-Cases`
- `/documentation/PackageDescription/Target/Dependency#Creating-a-Target-Dependency`
- `/documentation/PackageDescription/Target/Dependency/product(name:package:condition:)`
- `/documentation/PackageDescription/TargetDependencyCondition`
- `/documentation/PackageDescription/Package/Dependency`
- `/documentation/PackageDescription/Package/Dependency#Declaring-Requirements`
- `/documentation/PackageDescription/Package#Declaring-Supported-Platforms`
- `/documentation/PackageDescription/SupportedPlatform`
- `/documentation/PackageDescription/Package#Declaring-Supported-Languages`
- `/documentation/PackageDescription/SwiftSetting#Configuring-Swift-Settings`
- `/documentation/PackageDescription/SwiftSetting/defaultIsolation(_:_:)`
- `/documentation/Xcode/build-settings-reference#Default-Actor-Isolation`
- `/documentation/PackageDescription/Resource`
- `/documentation/PackageDescription/Resource/process(_:localization:)`
- `/documentation/PackageDescription/Resource/copy(_:)`
- `/documentation/Xcode/bundling-resources-with-a-swift-package`
- `/documentation/PackageDescription/Target#Creating-a-Binary-Target`
- `/documentation/PackageDescription/Target/binaryTarget(name:url:checksum:)`
- `/documentation/PackageDescription/Target/checksum`
- `/documentation/Swift/encoding-decoding-and-serialization#Custom-Encoding-and-Decoding`
- `/documentation/Swift/Encodable`
- `/documentation/Swift/Decodable`
- `/documentation/Swift/CodingKey`
- `/documentation/Swift/Sendable`
- `/documentation/Swift/Sendable#Sendable-Structures-and-Enumerations`
- `/documentation/Swift/Sendable#Sendable-Actors`
- `/documentation/Swift/concurrency#Actors`

## Evidence boundary

Xcode surfaced the manifest/API contracts above, but no single Swift-native article covering source, ABI, semantic-version, wire-schema, and host-test policy. Those procedures are original evidence checks. Availability search mainly surfaced Objective-C interoperability guidance, so this skill confines its claims to package floors, declaration availability, compile checks, and runtime fallback evidence.

Xcode DocumentationSearch did not settle `Package.resolved` precedence for reusable libraries. The leaf/top-level resolution boundary was checked separately against the official Swift Package Manager article [Resolving and updating dependencies](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/resolvingpackageversions/).
