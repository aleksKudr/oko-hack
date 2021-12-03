package org.tensorflow.lite.examples.classification

import ManagePermissions
import android.Manifest
import android.annotation.SuppressLint
import android.content.Context
import android.graphics.*
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.StrictMode
import android.os.StrictMode.ThreadPolicy
import android.util.Base64
import android.util.Log
import android.util.Size
import android.widget.Button
import android.widget.ImageView
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.*
import androidx.camera.core.Camera
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.core.content.ContextCompat
import androidx.lifecycle.Observer
import androidx.recyclerview.widget.RecyclerView
import khttp.responses.Response
import khttp.structures.files.FileLike
import org.json.JSONObject
import org.tensorflow.lite.examples.classification.ml.FlowerModel
import org.tensorflow.lite.examples.classification.ui.RecognitionAdapter
import org.tensorflow.lite.examples.classification.util.YuvToRgbConverter
import org.tensorflow.lite.examples.classification.viewmodel.Recognition
import org.tensorflow.lite.examples.classification.viewmodel.RecognitionListViewModel
import org.tensorflow.lite.gpu.CompatibilityList
import org.tensorflow.lite.support.image.TensorImage
import org.tensorflow.lite.support.model.Model
import org.tensorflow.lite.task.vision.detector.ObjectDetector
import java.io.ByteArrayOutputStream
import java.util.concurrent.Executors


// Constants
private const val MAX_RESULT_DISPLAY = 3 // Maximum number of results displayed
private const val TAG = "TFL Classify" // Name for logging
private const val REQUEST_CODE_PERMISSIONS = 999 // Return code after asking for permission

// permission needed
private var REQUIRED_PERMISSIONS = arrayOf(
    Manifest.permission.INTERNET,
    Manifest.permission.CAMERA
)
// Listener for the result of the ImageAnalyzer
typealias RecognitionListener = (recognition: List<Recognition>) -> Unit

private var LABELS = mutableListOf<Recognition>()
private var LABELS2: String = ""
private var OBJ: String = ""
private var IMAGE: String? = ""
private var IMAGEVIEW: String? = ""
private lateinit var inputImageView: ImageView


@Suppress("DEPRECATION")
class MainActivity : AppCompatActivity() {
    companion object {
        const val TAG = "TFLite - ODT"
        const val REQUEST_IMAGE_CAPTURE: Int = 1
        private const val MAX_FONT_SIZE = 96F
    }

    // CameraX variables
    private lateinit var preview: Preview // Preview use case, fast, responsive view of the camera
    private lateinit var imageAnalyzer: ImageAnalysis // Analysis use case, for running ML code
    private lateinit var camera: Camera
    private val cameraExecutor = Executors.newSingleThreadExecutor()


    // Views attachment
    private val resultRecyclerView by lazy {
        findViewById<RecyclerView>(R.id.recognitionResults) // Display the result of analysis
    }
    private val viewFinder by lazy {
        findViewById<PreviewView>(R.id.viewFinder) // Display the preview image from Camera
    }

    // Contains the recognition result. Since  it is a viewModel, it will survive screen rotations
    private val recogViewModel: RecognitionListViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        val PermissionsRequestCode = 123
        lateinit var managePermissions: ManagePermissions
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        inputImageView = findViewById(R.id.imageView)

        val list = listOf<String>(
            Manifest.permission.INTERNET,
            Manifest.permission.CAMERA

        )


        // Initialize a new instance of ManagePermissions class
        managePermissions = ManagePermissions(this, list, PermissionsRequestCode)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M)
            managePermissions.checkPermissions()


        val viewAdapter = RecognitionAdapter(this)
        resultRecyclerView.adapter = viewAdapter
        resultRecyclerView.itemAnimator = null
        recogViewModel.recognitionList.observe(this,
            Observer {
                viewAdapter.submitList(it)
            }
        )

        val btnStartCamera = findViewById<Button>(R.id.btn_start_camera)
        btnStartCamera.setOnClickListener {
            //Toast.makeText(this, "Clicked", Toast.LENGTH_SHORT).show()

            if (btnStartCamera.text == "Включить камеру") {
                btnStartCamera.text = "Сделать снимок и отправить"
                startCamera()

            } else if (btnStartCamera.text == "Сделать снимок и отправить") {
                btnStartCamera.text = "Включить камеру"
                val cameraProviderFuture = ProcessCameraProvider.getInstance(this)
                val cameraProvider: ProcessCameraProvider = cameraProviderFuture.get()
                cameraProvider.unbindAll()

                val policy = ThreadPolicy.Builder().permitAll().build()
                StrictMode.setThreadPolicy(policy)
                // http://httpbin.org/post
                // https://ptsv2.com/t/9t2bk-1638302502/post

                // Bitmap bmp = BitmapFactory.decodeByteArray(byteArray, 0, byteArray.length);


                val thread = Thread {

                    try {
//                        val stream = ByteArrayOutputStream()
//                        val tmp1 = StringToBitMap(IMAGEVIEW)
//                        if (tmp1 != null) {
//                            tmp1.compress(Bitmap.CompressFormat.PNG, 90, stream)
//                        }

                        val response: Response = khttp.post(
                            url = "http://oko.hack48.ru:8080/upload_image/",
                            data = mapOf("photo" to IMAGE))
                            //data = mapOf("username" to "root", "password" to "pass"))
                            //files = listOf(FileLike("image", stream.toByteArray())))
                            // files = listOf(FileLike("image", stream.toByteArray())))
                            //data = mapOf("classes" to LABELS.toString())//, "image" to IMAGE)
                        //)
                        //files = listOf(FileLike("image", stream.toByteArray())))

                        //data = mapOf("classes" to LABELS.toString())
                        val obj: JSONObject = response.jsonObject
                        var tmp: String
                        tmp = obj.toString()
                        OBJ = tmp

                    } catch (e: java.lang.Exception) {
                        OBJ = e.toString() //"Network error!"
                    }
                }
                thread.start()

                Toast.makeText(this, OBJ, Toast.LENGTH_SHORT).show()

                //Toast.makeText(this, LABELS.toString(), Toast.LENGTH_SHORT).show()
                //Toast.makeText(this, LABELS2.toString(), Toast.LENGTH_SHORT).show()

            }

        }
        val handler = Handler()
        handler.postDelayed(object : Runnable {
            override fun run() {
                runOnUiThread {
                    inputImageView.setImageBitmap(StringToBitMap(IMAGEVIEW))

                }
                handler.postDelayed(this, 1000)//1 sec delay
            }
        }, 0)


    }


    fun StringToBitMap(encodedString: String?): Bitmap? {
        return try {
            val encodeByte =
                Base64.decode(encodedString, Base64.DEFAULT)
            BitmapFactory.decodeByteArray(encodeByte, 0, encodeByte.size)
        } catch (e: java.lang.Exception) {
            e.message
            null
        }
    }


    /**
     * Start the Camera which involves:
     *
     * 1. Initialising the preview use case
     * 2. Initialising the image analyser use case
     * 3. Attach both to the lifecycle of this activity
     * 4. Pipe the output of the preview object to the PreviewView on the screen
     */
    private fun startCamera() {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(this)

        cameraProviderFuture.addListener(Runnable {
            // Used to bind the lifecycle of cameras to the lifecycle owner
            val cameraProvider: ProcessCameraProvider = cameraProviderFuture.get()

            preview = Preview.Builder()
                .build()


            imageAnalyzer = ImageAnalysis.Builder()
                // This sets the ideal size for the image to be analyse, CameraX will choose the
                // the most suitable resolution which may not be exactly the same or hold the same
                // aspect ratio
                .setTargetResolution(Size(224, 224))
                // How the Image Analyser should pipe in input, 1. every frame but drop no frame, or
                // 2. go to the latest frame and may drop some frame. The default is 2.
                // STRATEGY_KEEP_ONLY_LATEST. The following line is optional, kept here for clarity
                .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
                .build()
                .also { analysisUseCase: ImageAnalysis ->
                    analysisUseCase.setAnalyzer(cameraExecutor, ImageAnalyzer(this) { items ->
                        // updating the list of recognised objects
                        recogViewModel.updateData(items)
                    })
                }

            // Select camera, back is the default. If it is not available, choose front camera
            val cameraSelector =
                if (cameraProvider.hasCamera(CameraSelector.DEFAULT_BACK_CAMERA))
                    CameraSelector.DEFAULT_BACK_CAMERA else CameraSelector.DEFAULT_FRONT_CAMERA

            try {
                // Unbind use cases before rebinding
                cameraProvider.unbindAll()

                // Bind use cases to camera - try to bind everything at once and CameraX will find
                // the best combination.
                camera = cameraProvider.bindToLifecycle(
                    this, cameraSelector, preview, imageAnalyzer
                )

                // Attach the preview to preview view, aka View Finder
                preview.setSurfaceProvider(viewFinder.surfaceProvider)

            } catch (exc: Exception) {
                Log.e(TAG, "Use case binding failed", exc)
            }

        }, ContextCompat.getMainExecutor(this))
    }

    private class ImageAnalyzer(ctx: Context, private val listener: RecognitionListener) :
        ImageAnalysis.Analyzer {

        // TODO 1: Add class variable TensorFlow Lite Model
        // Initializing the flowerModel by lazy so that it runs in the same thread when the process
        // method is called.
        private val flowerModel: FlowerModel by lazy {

            // TODO 6. Optional GPU acceleration
            val compatList = CompatibilityList()

            val options = if (compatList.isDelegateSupportedOnThisDevice) {
                Log.d(TAG, "This device is GPU Compatible ")
                Model.Options.Builder().setDevice(Model.Device.GPU).build()
            } else {
                Log.d(TAG, "This device is GPU Incompatible ")
                Model.Options.Builder().setNumThreads(4).build()
            }

            // Initialize the Flower Model
            FlowerModel.newInstance(ctx, options)


        }

        val options = ObjectDetector.ObjectDetectorOptions.builder()
            .setMaxResults(5)
            .setScoreThreshold(0.3f)
            .build()
        val detector by lazy {
            ObjectDetector.createFromFileAndOptions(
                ctx,
                "detect.tflite",
                options
            )
        }

        fun bitMapToString(bitmap: Bitmap?): String? {
            val baos = ByteArrayOutputStream()
            if (bitmap != null) {
                bitmap.compress(Bitmap.CompressFormat.PNG, 100, baos)
            }
            val b = baos.toByteArray()

            return Base64.encodeToString(b, Base64.DEFAULT)
        }


        private fun drawDetectionResult(
            bitmap: Bitmap,
            detectionResults: List<DetectionResult>
        ): Bitmap {
            val outputBitmap = bitmap.copy(Bitmap.Config.ARGB_8888, true)
            val canvas = Canvas(outputBitmap)
            val pen = Paint()
            pen.textAlign = Paint.Align.LEFT

            detectionResults.forEach {
                // draw bounding box
                pen.color = Color.RED
                pen.strokeWidth = 8F
                pen.style = Paint.Style.STROKE
                val box = it.boundingBox
                canvas.drawRect(box, pen)


                val tagSize = Rect(0, 0, 0, 0)

                // calculate the right font size
                pen.style = Paint.Style.FILL_AND_STROKE
                pen.color = Color.YELLOW
                pen.strokeWidth = 2F

                pen.textSize = MAX_FONT_SIZE
                pen.getTextBounds(it.text, 0, it.text.length, tagSize)
                val fontSize: Float = pen.textSize * box.width() / tagSize.width()

                // adjust the font size so texts are inside the bounding box
                if (fontSize < pen.textSize) pen.textSize = fontSize

                var margin = (box.width() - tagSize.width()) / 2.0F
                if (margin < 0F) margin = 0F
                canvas.drawText(
                    it.text, box.left + margin,
                    box.top + tagSize.height().times(1F), pen
                )
            }
            return outputBitmap
        }

        override fun analyze(imageProxy: ImageProxy) {

            val items = mutableListOf<Recognition>()

            // TODO 2: Convert Image to Bitmap then to TensorImage
            val tfImage = TensorImage.fromBitmap(toBitmap(imageProxy))

            val results = detector.detect(tfImage)
            LABELS2 = results.toString()

            val resultToDisplay = results.map {
                // Get the top-1 category and craft the display text
                val category = it.categories.first()
                val text = "${category.label}, ${category.score.times(100).toInt()}%"

                // Create a data object to display the detection result
                DetectionResult(it.boundingBox, text)
            }
            // Draw the detection result on the bitmap and show it.
            val imgWithResult =
                toBitmap(imageProxy)?.let { drawDetectionResult(it, resultToDisplay) }
            IMAGEVIEW = bitMapToString(imgWithResult)

            // TODO 3: Process the image using the trained model, sort and pick out the top results
            val outputs = flowerModel.process(tfImage)
                .probabilityAsCategoryList.apply {
                    sortByDescending { it.score } // Sort with highest confidence first
                }.take(MAX_RESULT_DISPLAY) // take the top results

            // TODO 4: Converting the top probability items into a list of recognitions
            for (output in outputs) {
                items.add(Recognition(output.label, output.score))
            }

            try {
                IMAGE = bitMapToString(toBitmap(imageProxy))
            } catch (e: java.lang.Exception) {

            }
            // Return the result
            listener(items.toList())
            LABELS = items
            // Close the image,this tells CameraX to feed the next image to the analyzer
            imageProxy.close()


        }

        /**
         * Convert Image Proxy to Bitmap
         */
        private val yuvToRgbConverter = YuvToRgbConverter(ctx)
        private lateinit var bitmapBuffer: Bitmap
        private lateinit var rotationMatrix: Matrix

        @SuppressLint("UnsafeExperimentalUsageError")
        private fun toBitmap(imageProxy: ImageProxy): Bitmap? {

            val image = imageProxy.image ?: return null

            // Initialise Buffer
            if (!::bitmapBuffer.isInitialized) {
                // The image rotation and RGB image buffer are initialized only once
                Log.d(TAG, "Initalise toBitmap()")
                rotationMatrix = Matrix()
                rotationMatrix.postRotate(imageProxy.imageInfo.rotationDegrees.toFloat())
                bitmapBuffer = Bitmap.createBitmap(
                    imageProxy.width, imageProxy.height, Bitmap.Config.ARGB_8888
                )
            }

            // Pass image to an image analyser
            yuvToRgbConverter.yuvToRgb(image, bitmapBuffer)

            // Create the Bitmap in the correct orientation
            return Bitmap.createBitmap(
                bitmapBuffer,
                0,
                0,
                bitmapBuffer.width,
                bitmapBuffer.height,
                rotationMatrix,
                false
            )
        }

    }
}


data class DetectionResult(val boundingBox: RectF, val text: String)

