# Apple documentation reviewed

Reviewed with Xcode DocumentationSearch on **2026-08-30**. Re-run it and update `apple-docs-reviewed` after material SDK or App Store privacy changes. Apple sources do not define an OTLP provider’s retention or legal obligations.

Fresh query: `OSSignposter privacy interpolation SignpostMetadata MetricKit SignpostRecord DiagnosticReport signpostData Swift struct memberwise initializer access control`.

- [OSLogPrivacy](https://developer.apple.com/documentation/os/oslogprivacy) — redaction/visibility. Xcode URI: `/documentation/os/OSLogPrivacy`.
- [Privacy formatters](https://developer.apple.com/documentation/os/message-argument-formatters#Privacy-Options). Xcode URI: `/documentation/os/message-argument-formatters#Privacy-Options`.
- [Hash mask](https://developer.apple.com/documentation/os/oslogprivacy/mask/hash) — linkable local display. Xcode URI: `/documentation/os/OSLogPrivacy/Mask/hash`.
- [`OSSignposter`](https://developer.apple.com/documentation/os/OSSignposter), [`SignpostMetadata`](https://developer.apple.com/documentation/os/SignpostMetadata), and [`SignpostRecord`](https://developer.apple.com/documentation/MetricKit/SignpostRecord).
- [MetricKit diagnostic signpost data](https://developer.apple.com/documentation/MetricKit/DiagnosticReport/Environment-swift.struct#Signpost-data) and [custom metric logs](https://developer.apple.com/documentation/MetricKit/MetricManager#Custom-metric-logs).
- [MetricManager reports](https://developer.apple.com/documentation/metrickit/metricmanager#Reports). Xcode URI: `/documentation/MetricKit/MetricManager#Reports`.
- [metricReports](https://developer.apple.com/documentation/metrickit/metricmanager/metricreports). Xcode URI: `/documentation/MetricKit/MetricManager/metricReports`.
- [diagnosticReports](https://developer.apple.com/documentation/metrickit/metricmanager/diagnosticreports). Xcode URI: `/documentation/MetricKit/MetricManager/diagnosticReports`.
- [MXMetricManager API](https://developer.apple.com/documentation/metrickit/mxmetricmanager-api) — legacy API family. Xcode URI: `/documentation/MetricKit/MXMetricManager-API`.
- [Privacy manifest files](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files). Xcode URI: `/documentation/BundleResources/privacy-manifest-files`.
- [Describing collected data](https://developer.apple.com/documentation/bundleresources/describing-data-use-in-privacy-manifests). Xcode URI: `/documentation/BundleResources/describing-data-use-in-privacy-manifests`.
- [Required-reason APIs](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api). Xcode URI: `/documentation/BundleResources/describing-use-of-required-reason-api`.
- [TN3183](https://developer.apple.com/documentation/technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest). Xcode URI: `/documentation/Technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest`.

Redaction is not collection permission; this skill excludes prohibited content before all sinks. MetricKit origin does not authorize forwarding. Collected-data declarations apply across platforms, while required-reason scope follows Apple’s current named platforms.
