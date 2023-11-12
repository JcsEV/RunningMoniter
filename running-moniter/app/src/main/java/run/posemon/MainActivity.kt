/* Copyright 2022 Lin Yi. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================
*/

/** 本应用主要对 Tensorflow Lite Pose Estimation 示例项目的 MainActivity.kt
 *  文件进行了重写，示例项目中其余文件除了包名调整外基本无改动，原版权归
 *  The Tensorflow Authors 所有 */

package run.posemon

import android.Manifest
import android.annotation.SuppressLint
import android.app.AlertDialog
import android.app.Dialog
import android.content.pm.PackageManager
import android.os.Bundle
import android.os.Process
import android.view.SurfaceView
import android.view.View
import android.view.WindowManager
import android.widget.*
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.fragment.app.DialogFragment
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import run.posemon.camera.CameraSource
import run.posemon.data.Device
import run.posemon.data.Camera
import run.posemon.ml.ModelType
import run.posemon.ml.MoveNet
import run.posemon.ml.PoseClassifier

class MainActivity : AppCompatActivity() {
    companion object { private const val FRAGMENT_DIALOG = "dialog" }
    /** 为视频画面创建一个 SurfaceView */
    private lateinit var surfaceView: SurfaceView
    /** 修改默认计算设备：CPU、GPU、NNAPI（AI加速器） */
    private var device = Device.CPU
    /** 修改默认摄像头：FRONT、BACK */
    private var selectedCamera = Camera.BACK
    /** 定义几个计数器 */
    private var forrestgumpCounter = 0
    private var forwardrunCounter = 0
    private var girlrunCounter = 0
    private var narutoCounter = 0
    private var normalrunCounter = 0
    private var shoulderrunCounter = 0
    private var sitwithrunCounter = 0
    private var unswingingarmCounter = 0
    private var missingCounter = 0
    /** 定义一个历史姿态寄存器 */
    private var poseRegister = "NormalRun"
    /** 设置一个用来显示 Debug 信息的 TextView */
    private lateinit var tvDebug: TextView
    private lateinit var tvFPS: TextView
    private lateinit var tvScore: TextView
    private lateinit var spnDevice: Spinner
    private lateinit var spnCamera: Spinner
    private var cameraSource: CameraSource? = null
    private var isClassifyPose = true

    private val requestPermissionLauncher = registerForActivityResult(ActivityResultContracts.RequestPermission()) {
        isGranted: Boolean ->
        /** 得到用户相机授权后，程序开始运行 */
        if (isGranted) { openCamera() }
        /** 提示用户“未获得相机权限，应用无法运行” */
        else { ErrorDialog.newInstance(getString(R.string.tfe_pe_request_permission)).show(supportFragmentManager, FRAGMENT_DIALOG) }
    }

    private var changeDeviceListener = object : AdapterView.OnItemSelectedListener {
        override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) { changeDevice(position) }
        /** 如果用户未选择运算设备，使用默认设备进行计算 */
        override fun onNothingSelected(parent: AdapterView<*>?) {}
    }

    private var changeCameraListener = object : AdapterView.OnItemSelectedListener {
        override fun onItemSelected(p0: AdapterView<*>?, view: View?, direction: Int, id: Long) { changeCamera(direction) }
        /** 如果用户未选择摄像头，使用默认摄像头进行拍摄 */
        override fun onNothingSelected(p0: AdapterView<*>?) {}
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        /** 程序运行时保持屏幕常亮 */
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        tvScore = findViewById(R.id.tvScore)
        /** 用来显示 Debug 信息 */
        tvDebug = findViewById(R.id.tvDebug)
        tvFPS = findViewById(R.id.tvFps)
        spnDevice = findViewById(R.id.spnDevice)
        spnCamera = findViewById(R.id.spnCamera)
        surfaceView = findViewById(R.id.surfaceView)
        initSpinner()
        if (!isCameraPermissionGranted()) { requestPermission() }
    }

    override fun onStart() {
        super.onStart()
        openCamera()
    }

    override fun onResume() {
        cameraSource?.resume()
        super.onResume()
    }

    override fun onPause() {
        cameraSource?.close()
        cameraSource = null
        super.onPause()
    }

    /** 检查相机权限是否有授权 */
    private fun isCameraPermissionGranted(): Boolean {
        return checkPermission(Manifest.permission.CAMERA, Process.myPid(), Process.myUid()) == PackageManager.PERMISSION_GRANTED
    }

    private fun openCamera() {
        if (!isCameraPermissionGranted()) { return }
        if (cameraSource != null) {
            createPoseEstimator()
            return
        }
        cameraSource = CameraSource(surfaceView, selectedCamera, object : CameraSource.CameraSourceListener {
            /** 解释一下，tfe_pe_tv 的意思：tensorflow example、pose estimation、text view */
            override fun onFPSListener(fps: Int) {tvFPS.text = getString(R.string.tfe_pe_tv_fps, fps)}
            /** 对检测结果进行处理 */
            @SuppressLint("SetTextI18n")
            override fun onDetectedInfo(personScore: Float?, poseLabels: List<Pair<String, Float>>?) {
                tvScore.text = getString(R.string.tfe_pe_tv_score, personScore ?: 0f)
                /** 分析目标姿态，给出提示 */
                if (poseLabels != null && personScore != null && personScore > 0.3) {
                    missingCounter = 0
                    val sortedLabels = poseLabels.sortedByDescending { it.second }
                    when (sortedLabels[0].first) {
                        "ForrestGump" -> {
                            forwardrunCounter = 0
                            girlrunCounter = 0
                            narutoCounter = 0
                            normalrunCounter = 0
                            shoulderrunCounter = 0
                            sitwithrunCounter = 0
                            unswingingarmCounter = 0
                            if (poseRegister == "ForrestGump") { forrestgumpCounter++ }
                            poseRegister = "ForrestGump"
                            if (forrestgumpCounter > 5) { tvDebug.text = "ForrestGump" }
                            else if (forrestgumpCounter > 3) { tvDebug.text = "May ForrestGump" }
                        }
                        "ForwardRun" -> {
                            forrestgumpCounter = 0
                            girlrunCounter = 0
                            narutoCounter = 0
                            normalrunCounter = 0
                            shoulderrunCounter = 0
                            sitwithrunCounter = 0
                            unswingingarmCounter = 0
                            if (poseRegister == "ForwardRun") { forwardrunCounter++ }
                            poseRegister = "ForwardRun"
                            if (forwardrunCounter > 5) { tvDebug.text = "ForwardRun" }
                            else if (forwardrunCounter > 3) { tvDebug.text = "May ForwardRun" }
                        }
                        "GirlRun" -> {
                            forrestgumpCounter = 0
                            forwardrunCounter = 0
                            narutoCounter = 0
                            normalrunCounter = 0
                            shoulderrunCounter = 0
                            sitwithrunCounter = 0
                            unswingingarmCounter = 0
                            if (poseRegister == "GirlRun") { girlrunCounter++ }
                            poseRegister = "GirlRun"
                            if (girlrunCounter > 5) { tvDebug.text = "GirlRun" }
                            else if (girlrunCounter > 3) { tvDebug.text = "May GirlRun" }
                        }
                        "Naruto" -> {
                            forrestgumpCounter = 0
                            forwardrunCounter = 0
                            girlrunCounter = 0
                            normalrunCounter = 0
                            shoulderrunCounter = 0
                            sitwithrunCounter = 0
                            unswingingarmCounter = 0
                            if (poseRegister == "Naruto") { narutoCounter++ }
                            poseRegister = "Naruto"
                            if (narutoCounter > 5) { tvDebug.text = "Naruto" }
                            else if (narutoCounter > 3) { tvDebug.text = "May Naruto" }
                        }
                        "ShoulderRun" -> {
                            forrestgumpCounter = 0
                            forwardrunCounter = 0
                            girlrunCounter = 0
                            narutoCounter = 0
                            normalrunCounter = 0
                            sitwithrunCounter = 0
                            unswingingarmCounter = 0
                            if (poseRegister == "ShoulderRun") { shoulderrunCounter++ }
                            poseRegister = "ShoulderRun"
                            if (shoulderrunCounter > 5) { tvDebug.text = "ShoulderRun" }
                            else if (shoulderrunCounter > 3) { tvDebug.text = "May ShoulderRun" }
                        }
                        "SitWithRun" -> {
                            forrestgumpCounter = 0
                            forwardrunCounter = 0
                            girlrunCounter = 0
                            narutoCounter = 0
                            normalrunCounter = 0
                            shoulderrunCounter = 0
                            unswingingarmCounter = 0
                            if (poseRegister == "SitWithRun") { sitwithrunCounter++ }
                            poseRegister = "SitWithRun"
                            if (sitwithrunCounter > 5) { tvDebug.text = "SitWithRun" }
                            else if (sitwithrunCounter > 3) { tvDebug.text = "May SitWithRun" }
                        }
                        "UnswingingArm" -> {
                            forrestgumpCounter = 0
                            forwardrunCounter = 0
                            girlrunCounter = 0
                            narutoCounter = 0
                            normalrunCounter = 0
                            shoulderrunCounter = 0
                            sitwithrunCounter = 0
                            if (poseRegister == "UnswingingArm") { unswingingarmCounter++ }
                            poseRegister = "UnswingingArm"
                            if (unswingingarmCounter > 5) { tvDebug.text = "UnswingingArm" }
                            else if (unswingingarmCounter > 3) { tvDebug.text = "May UnswingingArm" }
                        }
                        else -> {
                            forrestgumpCounter = 0
                            forwardrunCounter = 0
                            girlrunCounter = 0
                            narutoCounter = 0
                            shoulderrunCounter = 0
                            sitwithrunCounter = 0
                            unswingingarmCounter = 0
                            if (poseRegister == "NormalRun") { normalrunCounter++ }
                            poseRegister = "NormalRun"
                            /** 显示当前坐姿状态：标准 */
                            if (normalrunCounter > 5) { tvDebug.text = "NormalRun" }
                        }
                    }
                }
                else {
                    missingCounter++
                    if (missingCounter > 5) { tvDebug.text = "No Person or Not Run" }
                }
            }
        })
        .apply { prepareCamera() }
        isPoseClassifier()
        lifecycleScope.launch(Dispatchers.Main) { cameraSource?.initCamera() }
        createPoseEstimator()
    }

    private fun isPoseClassifier() {
        cameraSource?.setClassifier(if (isClassifyPose) PoseClassifier.create(this) else null)
    }

    /** 初始化运算设备选项菜单（CPU、GPU） */
    private fun initSpinner() {
        ArrayAdapter.createFromResource(this, R.array.tfe_pe_device_name, android.R.layout.simple_spinner_item)
            .also { adapter -> adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
            spnDevice.adapter = adapter
            spnDevice.onItemSelectedListener = changeDeviceListener
        }
        ArrayAdapter.createFromResource(this, R.array.tfe_pe_camera_name, android.R.layout.simple_spinner_item)
            .also { adapter -> adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
            spnCamera.adapter = adapter
            spnCamera.onItemSelectedListener = changeCameraListener
        }
    }

    /** 在程序运行过程中切换运算设备 */
    private fun changeDevice(position: Int) {
        val targetDevice = when (position) {
            0 -> Device.CPU
            else -> Device.GPU
        }
        if (device == targetDevice) return
        device = targetDevice
        createPoseEstimator()
    }

    /** 在程序运行过程中切换摄像头 */
    private fun changeCamera(direaction: Int) {
        val targetCamera = when (direaction) {
            0 -> Camera.BACK
            else -> Camera.FRONT
        }
        if (selectedCamera == targetCamera) return
        selectedCamera = targetCamera
        cameraSource?.close()
        cameraSource = null
        openCamera()
    }

    private fun createPoseEstimator() {
        val poseDetector = MoveNet.create(this, device, ModelType.Thunder)
        poseDetector.let { detector -> cameraSource?.setDetector(detector) }
    }

    private fun requestPermission() {
        when (PackageManager.PERMISSION_GRANTED) {
            ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) -> { openCamera() }
            else -> { requestPermissionLauncher.launch(Manifest.permission.CAMERA) }
        }
    }

    /** 显示报错信息 */
    class ErrorDialog : DialogFragment() {
        override fun onCreateDialog(savedInstanceState: Bundle?): Dialog = AlertDialog.Builder(activity)
            .setMessage(requireArguments().getString(ARG_MESSAGE))
            .setPositiveButton(android.R.string.ok) { _, _ ->} // pass
            .create()
        companion object {
            @JvmStatic
            private val ARG_MESSAGE = "message"
            @JvmStatic
            fun newInstance(message: String): ErrorDialog = ErrorDialog().apply {
                arguments = Bundle().apply { putString(ARG_MESSAGE, message) }
            }
        }
    }
}
