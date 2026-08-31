# Apple documentation review

Last reviewed through Xcode `DocumentationSearch`: **2026-08-30**.

## Scope and freshness

This review covers modern Swift-native Vision text recognition and image classification, async image request performance with explicit orientation, ImageIO source inspection and incremental status, image extraction and destination finalization, image orientation and metadata, Uniform Type Identifiers for PNG, and Core Graphics/ColorSync color-space inspection.

The production limits, admission policy, deterministic validation, privacy rules, file/clipboard equivalence, and evidence contracts in this skill are application architecture. Apple documentation describes framework behavior but does not prescribe those limits or prove that a chosen pipeline is safe.

API names, availability, supported formats, request behavior, and model results can change with the SDK and OS. Re-run Xcode `DocumentationSearch` for the exact symbols in scope before updating `apple-docs-reviewed`. Verify deployment-target availability in the active Xcode SDK rather than inferring it from this reviewed URI list.

Fresh query used for this review: `RecognizeTextRequest ClassifyImageRequest availability legacy VNRecognizeTextRequest CGImageSourceGetType count incremental thumbnail transform max pixel size destination create type identifiers`.

## URIs consulted

Retrieved using Xcode MCP `DocumentationSearch`:

### Vision

- `/documentation/Vision/RecognizeTextRequest`
- `/documentation/Vision/VNRecognizeTextRequest`
- `/documentation/Vision/RecognizeTextRequest#Creating-a-request`
- `/documentation/Vision/RecognizeTextRequest/RecognitionLevel-swift.enum`
- `/documentation/Vision/RecognizeTextRequest/RecognitionLevel-swift.enum#Getting-the-recognition-levels`
- `/documentation/Vision/RecognizedTextObservation`
- `/documentation/Vision/RecognizedTextObservation#Getting-the-recognized-text`
- `/documentation/Vision/RecognizedTextObservation/topCandidates(_:)`
- `/documentation/Vision/RecognizedTextObservation#Inspecting-an-observation`
- `/documentation/Vision/RecognizedText`
- `/documentation/Vision/RecognizedText#Inspecting-the-recognized-text`
- `/documentation/Vision/RecognizedText/boundingBox(for:)`
- `/documentation/Vision/ClassifyImageRequest`
- `/documentation/Vision/VNClassifyImageRequest`
- `/documentation/Vision/ClassifyImageRequest#Creating-a-request`
- `/documentation/Vision/ClassifyImageRequest#Configuring-a-request`
- `/documentation/Vision/ClassifyImageRequest#Understanding-the-result`
- `/documentation/Vision/ClassificationObservation`
- `/documentation/Vision/ImageProcessingRequest#Performing-a-request`
- `/documentation/Vision/ImageProcessingRequest/perform(on:orientation:)-qxxx`
- `/documentation/Vision/locating-and-displaying-recognized-text#Perform-the-request`
- `/documentation/Vision/locating-and-displaying-recognized-text#Create-and-display-bounding-boxes`

### ImageIO and image properties

- `/documentation/ImageIO/CGImageSource#Creating-an-Image-Source`
- `/documentation/ImageIO/CGImageSourceCreateIncremental(_:)`
- `/documentation/ImageIO/CGImageSourceGetType(_:)`
- `/documentation/ImageIO/CGImageSourceGetCount(_:)`
- `/documentation/ImageIO/CGImageSource#Getting-the-Image-Status`
- `/documentation/ImageIO/CGImageSource#Updating-an-Incremental-Image`
- `/documentation/ImageIO/CGImageSourceUpdateData(_:_:_:)`
- `/documentation/ImageIO/CGImageSourceStatus`
- `/documentation/ImageIO/CGImageSource#Extracting-Images-From-an-Image-Source`
- `/documentation/ImageIO/CGImageSourceCreateImageAtIndex(_:_:_:)`
- `/documentation/ImageIO/CGImageSourceCreateThumbnailAtIndex(_:_:_:)`
- `/documentation/ImageIO/CGImageSource#Specifying-the-Read-Options`
- `/documentation/ImageIO/kCGImageSourceCreateThumbnailWithTransform`
- `/documentation/ImageIO/kCGImageSourceThumbnailMaxPixelSize`
- `/documentation/ImageIO/CGImageSourceCopyPropertiesAtIndex(_:_:_:)`
- `/documentation/ImageIO/CGImageSourceCopyMetadataAtIndex(_:_:_:)`
- `/documentation/ImageIO/CGImageSourceGetStatus(_:)`
- `/documentation/ImageIO/CGImageSourceGetStatusAtIndex(_:_:)`
- `/documentation/ImageIO/individual-image-properties`
- `/documentation/ImageIO/image-properties`
- `/documentation/ImageIO/image-properties#Image-Information`
- `/documentation/ImageIO/image-properties#Color-Information`
- `/documentation/ImageIO/CGImagePropertyOrientation`
- `/documentation/ImageIO/CGImagePropertyOrientation#Image-Orientations`
- `/documentation/ImageIO/CGImageDestination#Creating-an-Image-Destination`
- `/documentation/ImageIO/CGImageDestinationCreateWithData(_:_:_:_:)`
- `/documentation/ImageIO/CGImageDestination#Adding-Images-to-the-Destination`
- `/documentation/ImageIO/CGImageDestination#Finalizing-the-Image-Data`
- `/documentation/ImageIO/CGImageDestinationFinalize(_:)`
- `/documentation/ImageIO/CGImageDestination#Getting-the-Image-Types`
- `/documentation/ImageIO/CGImageDestinationCopyTypeIdentifiers()`

### Core Graphics, ColorSync, and type identifiers

- `/documentation/CoreGraphics/CGColorSpace`
- `/documentation/CoreGraphics/CGImage/bytesPerRow`
- `/documentation/CoreGraphics/CGImage/bitsPerPixel`
- `/documentation/CoreGraphics/CGColorSpace#Creating-Color-Spaces`
- `/documentation/CoreGraphics/CGColorSpace#Examining-a-Color-Space`
- `/documentation/ColorSync/color-profiles#Accessing-standard-RGB-profiles`
- `/documentation/UniformTypeIdentifiers/UTType-swift.struct#Images`
- `/documentation/UniformTypeIdentifiers/UTType-swift.struct/png`
